"""Signal preprocessing pipeline for the grid search.

Chains atomic SignalTransforms into an ordered pipeline that adds
new columns to the quarterly signal DataFrame before entry rules see it.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl

from abovedata_backtesting.processors.signal_transforms import SignalTransform


class IdentityPreprocessor:
    """Pass-through preprocessor that applies no transforms.

    Used as the baseline in grid search — represents "no preprocessing".
    """

    @property
    def name(self) -> str:
        return "identity"

    def params(self) -> dict[str, Any]:
        return {"preprocessor": "identity", "transforms": []}

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        return signals

    def output_columns(self) -> list[str]:
        return []

    @classmethod
    def grid(cls) -> list[IdentityPreprocessor]:
        return [cls()]


@dataclass(frozen=True, slots=True)
class SignalPreprocessor:
    """Ordered pipeline of signal transforms.

    Each transform adds new columns to the signal DataFrame.
    Transforms execute in order, so later transforms can reference
    columns created by earlier ones (e.g., TimeShift then WeightedBlend
    on the shifted column).

    Look-ahead bias safety:
    - Each transform is individually responsible for not using future data.
    - TimeShiftTransform enforces shift_quarters >= 1.
    - The pipeline validates that no transform overwrites original columns.
    """

    transforms: tuple[SignalTransform, ...]

    @property
    def name(self) -> str:
        if not self.transforms:
            return "identity"
        return "|".join(t.name for t in self.transforms)

    def params(self) -> dict[str, Any]:
        return {
            "preprocessor": self.name,
            "transforms": [t.params() for t in self.transforms],
        }

    def output_columns(self) -> list[str]:
        cols: list[str] = []
        for t in self.transforms:
            cols.extend(t.output_columns())
        return cols

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        """Apply all transforms in sequence.

        Validates that no original columns are overwritten.
        """
        original_cols = set(signals.columns)
        for transform in self.transforms:
            new_cols = set(transform.output_columns())
            overwritten = new_cols & original_cols
            if overwritten:
                raise ValueError(
                    f"Transform {transform.name} would overwrite original columns: "
                    f"{overwritten}. Transforms must create new columns only."
                )
            signals = transform.apply(signals, date_col)
        return signals

    @classmethod
    def grid(cls, transform_lists: list[list[SignalTransform]]) -> list[Self]:
        """Generate grid from lists of transform variations.

        Each element of transform_lists is a list of alternatives for that
        pipeline stage. The cartesian product produces all combinations.

        Example:
            SignalPreprocessor.grid([
                TimeShiftTransform.grid(
                    source_cols=[("visible_revenue_resid",)],
                    shift_quarters=[1, 2],
                ),
                RateOfChangeTransform.grid(
                    source_col=["visible_revenue_resid"],
                    lookback_quarters=[1],
                ),
            ])

        This produces preprocessors where each has one TimeShift variant
        AND one RateOfChange variant.
        """
        results: list[Self] = []
        for combo in product(*transform_lists):
            results.append(cls(transforms=tuple(combo)))
        return results
