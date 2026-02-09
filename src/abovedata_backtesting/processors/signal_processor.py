import datetime
from dataclasses import dataclass, field

import altair as alt
import numpy as np

# --- Visualization Layer ---
import polars as pl
from rich.console import Console
from statsmodels.tsa.seasonal import STL


def compute_stl_residuals_stable(
    df: pl.DataFrame, col: str, period: int = 4, min_burn_in: int = 8
) -> pl.Series:
    """
    Computes residuals using a stable anchored approach:
    1. Requires a minimum burn-in (e.g., 3 years) before generating signals.
    2. Uses a robust fit to ensure trend/seasonal components don't overreact
       to a single anomalous UCC filing.
    3. Normalizes the resulting residuals to maintain a consistent signal scale.
    """
    df = df.sort("earnings_date")
    vals = df[col].to_numpy()
    n = len(vals)
    residuals = [None] * n

    # We start only after we have enough data to define a 'regime'
    for i in range(min_burn_in, n):
        # Window includes all data from start to current T
        window_data = vals[: i + 1]

        # We use a longer trend window (trend=period*4+1) to force
        # the model to be 'stiff' and not follow the noise.
        stl = STL(
            window_data,
            period=period,
            seasonal=7,  # Fixed seasonal length for stability
            trend=13,  # Stiff trend to prevent 'End-point' wiggle
            robust=True,
        ).fit()

        # Capture the last residual
        res_val = stl.resid[-1]

        # Normalization Step:
        # Convert the raw residual into a Z-Score based on historical volatility.
        # This prevents the 'expanding window' from having scale-drift.
        prev_res_std = np.std(stl.resid[:-1]) if len(stl.resid) > 1 else 1.0
        residuals[i] = res_val / (prev_res_std + 1e-9)

    return pl.Series(f"{col}_resid", residuals)


@dataclass
class STLSignalProcessor:
    """
    Handles all Polars-based calculations and transformations.
    Includes 'Tactical' noise filtering to reduce false positives from small-window correlations.
    """

    df: pl.DataFrame
    ticker: str
    is_medical: bool
    visible_col: str  # The column containing unit counts
    ma_window: int = 4
    momentum_threshold: float = 0.5

    # NEW: Tactical Filter Constraints
    correlation_threshold: float = 0.8  # Only trust correlations above 0.8
    sigma_threshold: float = 1.0  # Signal must be > 1.0 std dev to matter

    df_signals_agg: pl.DataFrame = field(init=False)

    def process_by_segment(
        self, segment_col: str = "name", count_col: str = "count"
    ) -> pl.DataFrame:
        """
        Partitions data and ensures each segment uses its own unit count
        instead of the global visible_col.
        """
        if segment_col not in self.df.columns:
            return self.process()

        segments = self.df.partition_by(segment_col, maintain_order=True)
        processed_frames = []
        console = Console()

        for segment_df in segments:
            try:
                # We pass the filters down to the sub-processors
                sub_processor = STLSignalProcessor(
                    df=segment_df,
                    ticker=self.ticker,
                    visible_col=count_col,
                    ma_window=self.ma_window,
                    momentum_threshold=self.momentum_threshold,
                    correlation_threshold=self.correlation_threshold,
                    sigma_threshold=self.sigma_threshold,
                    is_medical=self.is_medical,
                )
                processed_frames.append(sub_processor.process())
            except pl.exceptions.InvalidOperationError:
                console.print_exception()
        return pl.concat(processed_frames)

    def process(self) -> pl.DataFrame:
        """Executes the full transformation pipeline with noise filtering."""
        return (
            self._ensure_sorted()
            ._apply_stl_decomposition()
            ._calculate_anomalous_correlations()
            ._enrich_with_rolling_stats()
            ._apply_noise_filter()
            ._identify_regime_shifts()
            .df.filter(pl.col("earnings_date").dt.year() >= 2015)
        )

    def _ensure_sorted(self) -> "STLSignalProcessor":
        self.df = self.df.sort("earnings_date")
        return self

    def _apply_stl_decomposition(self) -> "STLSignalProcessor":
        target_cols = [self.visible_col, "total_revenue", "consensus"]
        available_cols = [c for c in target_cols if c in self.df.columns]

        for col in available_cols:
            # Use expanding window STL to prevent look-ahead bias
            self.df = self.df.with_columns(
                # compute_stl_residuals_expanding(self.df, col, period=3)
                compute_stl_residuals_stable(self.df, col, period=4)
            )
        return self

    def _calculate_anomalous_correlations(self) -> "STLSignalProcessor":
        """
        Computes correlation series and calibrated magnitude predictions.
        """
        ucc_resid = f"{self.visible_col}_resid"
        rev_resid = "total_revenue_resid"

        self.df = (
            self.df.with_columns(
                # Realized surprise at T
                consensus_surprise=(
                    (pl.col("total_revenue") - pl.col("consensus"))
                    / pl.col("consensus")
                ),
                # Lagged residuals for point-in-time correlations
                total_revenue_resid_lag1=pl.col(rev_resid).shift(1),
                consensus_resid_lag1=pl.col("consensus_resid").shift(1),
            )
            .with_columns(
                consensus_beat=(pl.col("consensus_surprise") > 0),
                # Rolling standard deviations for calibration (point-in-time)
                ucc_resid_rolling_std=pl.col(ucc_resid)
                .shift(1)
                .rolling_std(self.ma_window, min_samples=2),
                rev_resid_rolling_std=pl.col(rev_resid)
                .shift(1)
                .rolling_std(self.ma_window, min_samples=2),
                surprise_rolling_mean=pl.col("consensus_surprise")
                .shift(1)
                .rolling_mean(self.ma_window, min_samples=2),
                surprise_rolling_std=pl.col("consensus_surprise")
                .shift(1)
                .rolling_std(self.ma_window, min_samples=2),
            )
            .with_columns(
                # 1. UCC ↔ Revenue (contemporaneous)
                pl.rolling_corr(
                    pl.col(ucc_resid).shift(1),
                    pl.col(rev_resid).shift(1),
                    window_size=self.ma_window,
                    min_samples=self.ma_window // 2,
                ).alias("contemp_corr_historical"),
                # 2. UCC ↔ Consensus
                pl.rolling_corr(
                    pl.col(ucc_resid).shift(1),
                    pl.col("consensus_resid").shift(1),
                    window_size=self.ma_window,
                    min_samples=self.ma_window // 2,
                ).alias("ucc_consensus_corr_historical"),
                # 3. Consensus ↔ Revenue
                pl.rolling_corr(
                    pl.col("consensus_resid").shift(1),
                    pl.col(rev_resid).shift(1),
                    window_size=self.ma_window,
                    min_samples=self.ma_window // 2,
                ).alias("consensus_revenue_corr_historical"),
                # 4. UCC ↔ Surprise
                pl.rolling_corr(
                    pl.col(ucc_resid).shift(1),
                    pl.col("consensus_surprise").shift(1),
                    window_size=self.ma_window,
                    min_samples=self.ma_window // 2,
                ).alias("ucc_surprise_corr_historical"),
                # LEADING correlation
                pl.rolling_corr(
                    pl.col(ucc_resid).shift(2),
                    pl.col(rev_resid).shift(1),
                    window_size=self.ma_window,
                    min_samples=self.ma_window // 2,
                ).alias("leading_corr_historical"),
            )
            .with_columns(
                # Regression coefficients: beta = corr × (std_y / std_x)
                ucc_to_rev_beta=(
                    pl.col("contemp_corr_historical")
                    * (
                        pl.col("rev_resid_rolling_std")
                        / (pl.col("ucc_resid_rolling_std") + 1e-9)
                    )
                ),
                ucc_to_surprise_beta=(
                    pl.col("ucc_surprise_corr_historical")
                    * (
                        pl.col("surprise_rolling_std")
                        / (pl.col("ucc_resid_rolling_std") + 1e-9)
                    )
                ),
            )
            .with_columns(
                # ORIGINAL PREDICTIONS (keep for backward compatibility):
                predicted_surprise_direction=(
                    pl.col(ucc_resid).sign() * pl.col("contemp_corr_historical").sign()
                ).cast(pl.Int8),
                predicted_surprise_magnitude=(
                    pl.col(ucc_resid) * pl.col("contemp_corr_historical")
                ),
                predicted_surprise_magnitude_v2=(
                    pl.col(ucc_resid) * pl.col("ucc_surprise_corr_historical")
                ),
                # CALIBRATED PREDICTIONS (new):
                predicted_rev_resid_calibrated=(
                    pl.col(ucc_resid) * pl.col("ucc_to_rev_beta")
                ),
                predicted_surprise_calibrated=(
                    pl.col(ucc_resid) * pl.col("ucc_to_surprise_beta")
                ),
            )
            .with_columns(
                # Original prediction errors (keep for backward compatibility)
                surprise_prediction_error=(
                    pl.col("consensus_surprise")
                    - pl.col("predicted_surprise_magnitude")
                ).abs(),
                surprise_prediction_error_v2=(
                    pl.col("consensus_surprise")
                    - pl.col("predicted_surprise_magnitude_v2")
                ).abs(),
                # Calibrated prediction error
                surprise_prediction_error_calibrated=(
                    pl.col("consensus_surprise")
                    - pl.col("predicted_surprise_calibrated")
                ).abs(),
                # Confidence bounds (±1 std of historical surprise)
                predicted_surprise_upper=(
                    pl.col("predicted_surprise_calibrated")
                    + pl.col("surprise_rolling_std")
                ),
                predicted_surprise_lower=(
                    pl.col("predicted_surprise_calibrated")
                    - pl.col("surprise_rolling_std")
                ),
            )
        )

        return self

    def _enrich_with_rolling_stats(self) -> "STLSignalProcessor":
        """
        Computes rolling statistics for both correlation series.
        All calculations use only historically available data.
        """
        ucc_resid = f"{self.visible_col}_resid"

        self.df = self.df.with_columns(
            # Smoothed correlations (reduce noise in the correlation estimates)
            pl.col("contemp_corr_historical")
            .rolling_mean(self.ma_window)
            .alias("contemp_corr_ma"),
            pl.col("leading_corr_historical")
            .rolling_mean(self.ma_window)
            .alias("leading_corr_ma"),
            # Signal volatility (same for both - it's the UCC residual volatility)
            pl.col(ucc_resid)
            .shift(1)  # Use only historical volatility
            .rolling_std(self.ma_window)
            .alias("signal_volatility_std"),
            # Correlation momentum (detect regime changes)
            (
                pl.col("contemp_corr_historical")
                - pl.col("contemp_corr_historical").shift(1)
            ).alias("contemp_corr_momentum"),
            (
                pl.col("leading_corr_historical")
                - pl.col("leading_corr_historical").shift(1)
            ).alias("leading_corr_momentum"),
        )
        return self

    def _apply_noise_filter(self) -> "STLSignalProcessor":
        """
        Confidence based on:
        1. Signal percentile (is UCC residual unusual?)
        2. Correlation strength (is UCC-Revenue relationship reliable?)

        Requires BOTH correlation > 0.3 AND signal_percentile > 0.3 to avoid trivial hits.
        Leading signal computed for analysis but not recommended for trading.
        """
        ucc_resid = f"{self.visible_col}_resid"

        self.df = (
            self.df.with_columns(
                ucc_resid_abs=pl.col(ucc_resid).abs(),
            )
            .with_columns(
                signal_percentile=(
                    pl.col("ucc_resid_abs").rank(method="ordinal")
                    / pl.col("ucc_resid_abs").len()
                ),
            )
            .with_columns(
                # Contemporaneous confidence
                contemp_confidence=pl.when(
                    (pl.col("contemp_corr_historical").abs() > 0.3)
                    & (pl.col("signal_percentile") > 0.3)
                )
                .then(
                    (
                        pl.col("contemp_corr_historical").fill_null(0).abs()
                        / self.correlation_threshold
                    ).clip(0, 1)
                    * pl.col("signal_percentile")
                )
                .otherwise(0.0),
                # Leading confidence (for analysis, not trading)
                leading_confidence=pl.when(
                    (pl.col("leading_corr_historical").abs() > 0.3)
                    & (pl.col("signal_percentile") > 0.3)
                )
                .then(
                    (
                        pl.col("leading_corr_historical").fill_null(0).abs()
                        / self.correlation_threshold
                    ).clip(0, 1)
                    * pl.col("signal_percentile")
                )
                .otherwise(0.0),
                # Filtered correlations
                filtered_contemp_corr=pl.when(
                    pl.col("contemp_corr_historical").abs() >= 0.1
                )
                .then(pl.col("contemp_corr_historical"))
                .otherwise(None),
                filtered_leading_corr=pl.when(
                    pl.col("leading_corr_historical").abs() >= 0.1
                )
                .then(pl.col("leading_corr_historical"))
                .otherwise(None),
            )
            .drop("ucc_resid_abs")
        )

        return self

    def _identify_regime_shifts(self) -> "STLSignalProcessor":
        """
        Detects regime shifts in both correlation series.
        A regime shift = sign flip + sufficient momentum + non-null signal.
        """
        self.df = self.df.with_columns(
            # Contemporaneous regime shifts
            pl.when(
                (
                    pl.col("filtered_contemp_corr").sign()
                    != pl.col("filtered_contemp_corr").shift(1).sign()
                )
                & (pl.col("contemp_corr_momentum").abs() > self.momentum_threshold)
                & pl.col("filtered_contemp_corr").is_not_null()
            )
            .then(pl.lit("Regime Shift"))
            .otherwise(None)
            .alias("contemp_regime_shift"),
            # Leading regime shifts
            pl.when(
                (
                    pl.col("filtered_leading_corr").sign()
                    != pl.col("filtered_leading_corr").shift(1).sign()
                )
                & (pl.col("leading_corr_momentum").abs() > self.momentum_threshold)
                & pl.col("filtered_leading_corr").is_not_null()
            )
            .then(pl.lit("Regime Shift"))
            .otherwise(None)
            .alias("leading_regime_shift"),
        )
        return self

    def select_top_signals(
        self, df: pl.DataFrame, segment_col: str, top_n: int = 5
    ) -> pl.DataFrame:
        """Filters for the top 5 segments based on highest absolute residual correlation."""
        self.df_signals_agg = (
            # Remove any nulls and low count items.
            df.filter(
                pl.col("contemp_corr_historical").is_between(-0.99, 0.99),
                pl.col("total_universe").gt(10),
            )
            .sort([segment_col, "earnings_date"])
            .group_by(segment_col)
            .agg(
                pl.col("contemp_corr_historical")
                .tail(5)
                .abs()
                .mean()
                .alias("abs_corr"),
                pl.len().alias("number_of_quarters"),
                pl.col("earnings_date").max(),
                mean_count := pl.col("count").mean().alias("mean_count"),
                # New metric: logic checks how many of the LAST 5 quarters exceed the mean
                quarters_above_mean=pl.col("count")
                .tail(top_n)
                .filter(pl.col("count").tail(top_n) > mean_count)
                .len(),
                # Alternative: strict volume check on the last 5
                recent_min_vol=pl.col("count")
                .tail(top_n)
                .min()
                .alias("recent_min_volume"),
            )
            .with_columns(
                (datetime.datetime.now().date() - pl.col("earnings_date"))  # type: ignore
                .dt.total_days()
                .alias("days_since_today"),
            )
            # Where the most recent data point is within the last year.
            # We only have consensus revenue until end of last year, so need to
            # go up to 1.5 years ago.
            .filter(pl.col("days_since_today") < (365 + 180))
            .sort("abs_corr", descending=True)
        )

        min_volume_cutoff = 0 if self.is_medical else 10
        mean_count = 4 if self.is_medical else 10
        number_quarters = 1 if self.is_medical else 4

        top_names = (
            self.df_signals_agg.filter(
                pl.col("number_of_quarters").gt(
                    number_quarters
                ),  # Number of quarters of data.
                pl.col("mean_count").gt(mean_count),
                pl.col("recent_min_vol").gt(min_volume_cutoff),
                pl.col("abs_corr").gt(0.3),
                # pl.col("quarters_above_mean") >= 3,  # Ensure consistency in the tail
            )
            .head(top_n)[segment_col]
            .to_list()
        )

        return df.filter(pl.col(segment_col).is_in(top_names)).sort(["earnings_date"])


class STLSignalVisualizer:
    """Encapsulates Altair dashboard generation."""

    @staticmethod
    def create_correlation_panel(
        df: pl.DataFrame,
        y_col: str,
        confidence_col: str,
        ticker: str,
        signal_name: str,
        target_name: str,
        color: str = "#5DA5DA",
        window: int = 4,
    ) -> alt.Chart:
        """
        Correlation time series with std deviation band, trend line,
        and confidence-encoded scatter points.
        """
        chart_df = df

        base = alt.Chart(chart_df).encode(
            x=alt.X("earnings_date:T", timeUnit="yearquarter", title="Quarter"),
        )

        # Rolling stats for band and trend
        transformed = base.transform_window(
            rolling_mean=f"mean({y_col})",
            rolling_std=f"stdev({y_col})",
            frame=[-window + 1, 0],
            sort=[{"field": "earnings_date"}],
        ).transform_calculate(
            upper_band="datum.rolling_mean + datum.rolling_std",
            lower_band="datum.rolling_mean - datum.rolling_std",
        )

        # Zero reference
        zero_line = (
            alt.Chart(pl.DataFrame({"y": [0]}))
            .mark_rule(color="gray", strokeDash=[2, 2], opacity=0.3)
            .encode(y="y:Q")
        )

        # ±1 Std Dev band
        band = transformed.mark_area(opacity=0.08, color=color).encode(
            y=alt.Y(
                "lower_band:Q",
                title="Correlation",
                scale=alt.Scale(domain=[-1.15, 1.15]),
            ),
            y2="upper_band:Q",
        )

        # Rolling mean trend (dashed)
        trend = transformed.mark_line(
            size=1.5, color=color, strokeDash=[6, 3], opacity=0.4
        ).encode(y="rolling_mean:Q")

        # Confidence scatter points (primary visual — no connector line)
        points = base.mark_circle(color=color).encode(
            y=alt.Y(f"{y_col}:Q"),
            size=alt.Size(
                f"{confidence_col}:Q",
                scale=alt.Scale(domain=[0, 1], range=[20, 120]),
                legend=None,
            ),
            opacity=alt.Opacity(
                f"{confidence_col}:Q",
                scale=alt.Scale(domain=[0, 1], range=[0.3, 1.0]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("earnings_date:T", title="Quarter"),
                alt.Tooltip(f"{y_col}:Q", title="Correlation", format=".2f"),
                alt.Tooltip(f"{confidence_col}:Q", title="Confidence", format=".2f"),
            ],
        )

        chart = alt.layer(
            zero_line,
            band,
            trend,
            points,
        ).properties(
            height=380,
            width=520,
            title={
                "text": f"{ticker}: {signal_name} → {target_name}",
                "subtitle": [
                    "Each point = one quarter. Larger/brighter points = higher confidence signals.",
                    f"Dashed line: {window}Q moving average trend.",
                    "Confidence = correlation strength × signal magnitude (both must exceed minimums).",
                ],
                "anchor": "start",
                "fontSize": 16,
                "subtitleFontSize": 11,
                "subtitleColor": "#999999",
            },
        )

        return chart

    @staticmethod
    def create_benchmark_panel(
        df: pl.DataFrame,
        ticker: str,
    ) -> alt.Chart:
        """
        Compares UCC signal vs analyst consensus correlation with revenue.
        """
        chart_df = df

        base = alt.Chart(chart_df).encode(
            x=alt.X("earnings_date:T", timeUnit="yearquarter", title="Quarter"),
        )

        zero_line = (
            alt.Chart(pl.DataFrame({"y": [0]}))
            .mark_rule(color="gray", strokeDash=[2, 2], opacity=0.3)
            .encode(y="y:Q")
        )

        # UCC points
        ucc_points = base.mark_circle(size=40, color="#5DA5DA").encode(
            y=alt.Y(
                "contemp_corr_historical:Q",
                title="Correlation with Revenue",
                scale=alt.Scale(domain=[-1.15, 1.15]),
            ),
            opacity=alt.Opacity(
                "contemp_confidence:Q",
                scale=alt.Scale(domain=[0, 1], range=[0.3, 1.0]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("earnings_date:T", title="Quarter"),
                alt.Tooltip("contemp_corr_historical:Q", title="UCC→Rev", format=".2f"),
                alt.Tooltip(
                    "consensus_revenue_corr_historical:Q",
                    title="Analyst→Rev",
                    format=".2f",
                ),
            ],
        )

        # Analyst points
        analyst_points = base.mark_point(
            size=35, shape="diamond", color="#F15854", filled=True, opacity=0.7
        ).encode(
            y="consensus_revenue_corr_historical:Q",
        )

        chart = alt.layer(
            zero_line,
            ucc_points,
            analyst_points,
        ).properties(
            height=380,
            width=580,
            title={
                "text": f"{ticker}: UCC Signal vs. Analyst Consensus",
                "subtitle": [
                    "Blue circles: UCC→Revenue correlation. Red diamonds: Consensus→Revenue correlation.",
                    "When blue is further from zero than red, UCC captures information analysts miss.",
                ],
                "anchor": "start",
                "fontSize": 16,
                "subtitleFontSize": 11,
                "subtitleColor": "#999999",
            },
        )

        return chart
