"""Tests for signal transforms and preprocessor pipeline.

Focuses on:
1. Look-ahead bias safety (shift_quarters >= 1 enforced)
2. Correct shift semantics (row T gets value from T-N)
3. Transform output column naming
4. Preprocessor pipeline validation (no column overwrites)
5. Grid generation
"""

from datetime import date

import polars as pl
import pytest

from abovedata_backtesting.processors.signal_preprocessor import (
    IdentityPreprocessor,
    SignalPreprocessor,
)
from abovedata_backtesting.processors.signal_transforms import (
    AccelerationTransform,
    CrossSignalRatioTransform,
    DifferenceTransform,
    RateOfChangeTransform,
    TimeShiftTransform,
    WeightedBlendTransform,
    ZScoreNormalizeTransform,
)


@pytest.fixture
def sample_signals() -> pl.DataFrame:
    """Quarterly signal DataFrame with known values."""
    return pl.DataFrame(
        {
            "earnings_date": [
                date(2020, 3, 31),
                date(2020, 6, 30),
                date(2020, 9, 30),
                date(2020, 12, 31),
                date(2021, 3, 31),
                date(2021, 6, 30),
            ],
            "visible_revenue_resid": [1.0, -0.5, 2.0, -1.0, 0.5, 1.5],
            "consensus_resid": [0.5, -0.3, 1.0, -0.8, 0.2, 0.7],
        }
    )


# ============================================================================
# TimeShiftTransform
# ============================================================================


class TestTimeShiftTransform:
    def test_shift_quarters_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="shift_quarters must be >= 1"):
            TimeShiftTransform(source_cols=("visible_revenue_resid",), shift_quarters=0)

    def test_shift_quarters_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="shift_quarters must be >= 1"):
            TimeShiftTransform(
                source_cols=("visible_revenue_resid",), shift_quarters=-1
            )

    def test_shift_1q_values(self, sample_signals: pl.DataFrame) -> None:
        t = TimeShiftTransform(source_cols=("visible_revenue_resid",), shift_quarters=1)
        result = t.apply(sample_signals)

        assert "visible_revenue_resid_lag1q" in result.columns
        lagged = result["visible_revenue_resid_lag1q"].to_list()

        # Row 0 (Q1 2020): no prior -> null
        assert lagged[0] is None
        # Row 1 (Q2 2020): should have Q1's value (1.0)
        assert lagged[1] == 1.0
        # Row 2 (Q3 2020): should have Q2's value (-0.5)
        assert lagged[2] == -0.5
        # Row 3 (Q4 2020): should have Q3's value (2.0)
        assert lagged[3] == 2.0

    def test_shift_2q_values(self, sample_signals: pl.DataFrame) -> None:
        t = TimeShiftTransform(source_cols=("visible_revenue_resid",), shift_quarters=2)
        result = t.apply(sample_signals)

        assert "visible_revenue_resid_lag2q" in result.columns
        lagged = result["visible_revenue_resid_lag2q"].to_list()

        # Rows 0-1: null (not enough history)
        assert lagged[0] is None
        assert lagged[1] is None
        # Row 2 (Q3 2020): should have Q1's value (1.0)
        assert lagged[2] == 1.0
        # Row 3 (Q4 2020): should have Q2's value (-0.5)
        assert lagged[3] == -0.5

    def test_multiple_cols(self, sample_signals: pl.DataFrame) -> None:
        t = TimeShiftTransform(
            source_cols=("visible_revenue_resid", "consensus_resid"),
            shift_quarters=1,
        )
        result = t.apply(sample_signals)
        assert "visible_revenue_resid_lag1q" in result.columns
        assert "consensus_resid_lag1q" in result.columns

    def test_output_columns(self) -> None:
        t = TimeShiftTransform(
            source_cols=("visible_revenue_resid", "consensus_resid"),
            shift_quarters=2,
        )
        assert t.output_columns() == [
            "visible_revenue_resid_lag2q",
            "consensus_resid_lag2q",
        ]

    def test_grid(self) -> None:
        transforms = TimeShiftTransform.grid(
            source_cols=[("visible_revenue_resid",)],
            shift_quarters=[1, 2],
        )
        assert len(transforms) == 2
        assert transforms[0].shift_quarters == 1
        assert transforms[1].shift_quarters == 2

    def test_missing_col_is_noop(self, sample_signals: pl.DataFrame) -> None:
        t = TimeShiftTransform(source_cols=("nonexistent_col",), shift_quarters=1)
        result = t.apply(sample_signals)
        assert "nonexistent_col_lag1q" not in result.columns


# ============================================================================
# RateOfChangeTransform
# ============================================================================


class TestRateOfChangeTransform:
    def test_roc_values(self, sample_signals: pl.DataFrame) -> None:
        t = RateOfChangeTransform(
            source_col="visible_revenue_resid", lookback_quarters=1
        )
        result = t.apply(sample_signals)
        assert "visible_revenue_resid_roc1q" in result.columns

        roc = result["visible_revenue_resid_roc1q"].to_list()
        # Row 0: null (no prior)
        assert roc[0] is None
        # Row 1: (-0.5 - 1.0) / (|1.0| + eps) ≈ -1.5
        assert abs(roc[1] - (-1.5)) < 0.01

    def test_output_columns(self) -> None:
        t = RateOfChangeTransform(source_col="x", lookback_quarters=2)
        assert t.output_columns() == ["x_roc2q"]


# ============================================================================
# AccelerationTransform
# ============================================================================


class TestAccelerationTransform:
    def test_output_columns(self) -> None:
        t = AccelerationTransform(source_col="x", lookback_quarters=1)
        assert t.output_columns() == ["x_accel1q"]

    def test_produces_values(self, sample_signals: pl.DataFrame) -> None:
        t = AccelerationTransform(
            source_col="visible_revenue_resid", lookback_quarters=1
        )
        result = t.apply(sample_signals)
        assert "visible_revenue_resid_accel1q" in result.columns
        # First two rows should be null (need 2 prior values for acceleration)
        accel = result["visible_revenue_resid_accel1q"].to_list()
        assert accel[0] is None
        assert accel[1] is None


# ============================================================================
# CrossSignalRatioTransform
# ============================================================================


class TestCrossSignalRatioTransform:
    def test_ratio_values(self, sample_signals: pl.DataFrame) -> None:
        t = CrossSignalRatioTransform(
            numerator_col="visible_revenue_resid",
            denominator_col="consensus_resid",
        )
        result = t.apply(sample_signals)
        col = "visible_revenue_resid_over_consensus_resid"
        assert col in result.columns
        ratios = result[col].to_list()
        # Row 0: 1.0 / (|0.5| + eps) ≈ 2.0
        assert abs(ratios[0] - 2.0) < 0.01


# ============================================================================
# WeightedBlendTransform
# ============================================================================


class TestWeightedBlendTransform:
    def test_blend(self, sample_signals: pl.DataFrame) -> None:
        # First create lag1q column
        shifted = TimeShiftTransform(
            source_cols=("visible_revenue_resid",), shift_quarters=1
        ).apply(sample_signals)

        t = WeightedBlendTransform(
            col_a="visible_revenue_resid",
            col_b="visible_revenue_resid_lag1q",
            weight_a=0.7,
        )
        result = t.apply(shifted)
        col = "blend_visible_revenue_resid_visible_revenue_resid_lag1q_w0.7"
        assert col in result.columns

        vals = result[col].to_list()
        # Row 1: 0.7 * (-0.5) + 0.3 * (1.0) = -0.35 + 0.3 = -0.05
        assert vals[0] is None  # lag1q is null
        assert abs(vals[1] - (-0.05)) < 0.01


# ============================================================================
# DifferenceTransform
# ============================================================================


class TestDifferenceTransform:
    def test_diff(self, sample_signals: pl.DataFrame) -> None:
        shifted = TimeShiftTransform(
            source_cols=("visible_revenue_resid",), shift_quarters=1
        ).apply(sample_signals)

        t = DifferenceTransform(
            col_a="visible_revenue_resid",
            col_b="visible_revenue_resid_lag1q",
        )
        result = t.apply(shifted)
        col = "diff_visible_revenue_resid_visible_revenue_resid_lag1q"
        assert col in result.columns

        vals = result[col].to_list()
        # Row 1: -0.5 - 1.0 = -1.5
        assert vals[0] is None
        assert abs(vals[1] - (-1.5)) < 0.01


# ============================================================================
# ZScoreNormalizeTransform
# ============================================================================


class TestZScoreNormalizeTransform:
    def test_output_columns(self) -> None:
        t = ZScoreNormalizeTransform(source_col="x")
        assert t.output_columns() == ["x_znorm"]

    def test_produces_values(self, sample_signals: pl.DataFrame) -> None:
        t = ZScoreNormalizeTransform(source_col="visible_revenue_resid", min_periods=2)
        result = t.apply(sample_signals)
        assert "visible_revenue_resid_znorm" in result.columns


# ============================================================================
# IdentityPreprocessor
# ============================================================================


class TestIdentityPreprocessor:
    def test_passthrough(self, sample_signals: pl.DataFrame) -> None:
        pp = IdentityPreprocessor()
        result = pp.apply(sample_signals)
        assert result.equals(sample_signals)
        assert pp.name == "identity"
        assert pp.output_columns() == []

    def test_grid(self) -> None:
        pps = IdentityPreprocessor.grid()
        assert len(pps) == 1
        assert pps[0].name == "identity"


# ============================================================================
# SignalPreprocessor
# ============================================================================


class TestSignalPreprocessor:
    def test_pipeline(self, sample_signals: pl.DataFrame) -> None:
        pp = SignalPreprocessor(
            transforms=(
                TimeShiftTransform(
                    source_cols=("visible_revenue_resid",), shift_quarters=1
                ),
                RateOfChangeTransform(
                    source_col="visible_revenue_resid", lookback_quarters=1
                ),
            )
        )
        result = pp.apply(sample_signals)
        assert "visible_revenue_resid_lag1q" in result.columns
        assert "visible_revenue_resid_roc1q" in result.columns

    def test_rejects_column_overwrite(self, sample_signals: pl.DataFrame) -> None:
        """Ensure preprocessor rejects transforms that overwrite original columns."""

        class BadTransform(RateOfChangeTransform):
            def output_columns(self) -> list[str]:
                return ["visible_revenue_resid"]  # overwrites original!

        pp = SignalPreprocessor(
            transforms=(
                BadTransform(source_col="visible_revenue_resid", lookback_quarters=1),
            )
        )
        with pytest.raises(ValueError, match="overwrite original columns"):
            pp.apply(sample_signals)

    def test_grid_generation(self) -> None:
        pps = SignalPreprocessor.grid(
            [
                TimeShiftTransform.grid(
                    source_cols=[("visible_revenue_resid",)],
                    shift_quarters=[1, 2],
                ),
                RateOfChangeTransform.grid(
                    source_col=["visible_revenue_resid"],
                    lookback_quarters=[1],
                ),
            ]
        )
        # 2 time shifts × 1 roc = 2 preprocessors
        assert len(pps) == 2
        assert len(pps[0].transforms) == 2
        assert len(pps[1].transforms) == 2

    def test_name_uniqueness(self) -> None:
        pp1 = SignalPreprocessor(
            transforms=(
                TimeShiftTransform(
                    source_cols=("visible_revenue_resid",), shift_quarters=1
                ),
            )
        )
        pp2 = SignalPreprocessor(
            transforms=(
                TimeShiftTransform(
                    source_cols=("visible_revenue_resid",), shift_quarters=2
                ),
            )
        )
        assert pp1.name != pp2.name
