import arrow
import pandas as pd
from typing import List

from pandas import DataFrame
from data.insights.insight import Insight
from data.models import InsightResult

class PriceAction(Insight):
    def __init__(self, day_lookback=30) -> None:
        self.day_lookback = day_lookback

    def generate(self, datum: DataFrame) -> List[InsightResult]:
        results = []
        df = datum[(datum['name'] == 'CLOSE') | (datum['name'] == 'VOLUME')].tail(self.day_lookback).copy()

        df['date'] = pd.to_datetime(df['date'])
        grouped = df.groupby('date')

        for date, group in grouped:
            price = group[group['name'] == 'CLOSE']['value'].to_list()[0]

            price = round(price, 2)
            volume = group[group['name'] == 'VOLUME']['value'].to_list()[0]

            results.append(
                InsightResult(
                    'Price/Volume',
                    f'{price}/{volume}',
                    arrow.get(date),
                    group.iloc[0, 3],
                    prompt_func=self._action_prompt
                )
            )

        return results

    @staticmethod
    def _action_prompt(insight: InsightResult):
        date = insight.date.format('MMM DD, YYYY')
        return f'{insight.symbol} Price/Volume {date} {insight.value}'