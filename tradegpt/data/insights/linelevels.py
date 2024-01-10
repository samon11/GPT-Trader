import arrow
from typing import List

from pandas import DataFrame
from data.insights.insight import Insight
from data.models import InsightResult

class LineLevels(Insight):
    def __init__(self, n_levels, day_lookback) -> None:
        self.n_levels = n_levels
        self.day_lookback = day_lookback
        super().__init__("Line Levels", self.day_lookback)

    def generate(self, datum: DataFrame) -> List[InsightResult]:
        results = []

        lows = datum[datum['name'] == 'LOW'].copy()
        highs = datum[datum['name'] == 'HIGH'].copy()

        support_levels = lows[lows['value'] < lows['value'].shift(1)][lows['value'] < lows['value'].shift(-1)].dropna()
        support_levels['value'] = support_levels['value'].astype(float)

        resistance_levels = highs[highs['value'] > highs['value'].shift(1)][highs['value'] > highs['value'].shift(-1)].dropna()
        resistance_levels['value'] = resistance_levels['value'].astype(float)

        for _, support in support_levels.nsmallest(self.n_levels, 'value').iterrows():
            results.append(
                InsightResult(
                    "Support",
                    support['value'],
                    arrow.get(support['date']),
                    support['symbol']
                )
            )

        for _, resistance in resistance_levels.nlargest(self.n_levels, 'value').iterrows():
            results.append(
                InsightResult(
                    "Resistance",
                    resistance['value'],
                    arrow.get(resistance['date']),
                    resistance['symbol']
                )
            )

        return results
