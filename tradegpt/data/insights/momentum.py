import arrow
import pandas as pd
from typing import List
from data.insights.insight import Insight
from data.models import InsightResult


class Momentum(Insight):
    def __init__(self, width=20, most_recent=False) -> None:
        self.width = width
        self.most_recent = most_recent
        super().__init__(f"Bollinger Bands {self.width}", self.width * 4)

    def generate(self, datum: pd.DataFrame) -> List[InsightResult]:
        results = []
        df = datum[datum['name'] == "CLOSE"].copy()
        df['sma'] = df['value'].rolling(self.width).mean()
        df['std'] = df['value'].rolling(self.width).std()
        df['upper'] = df['sma'] + (2 * df['std'])
        df['lower'] = df['sma'] - (2 * df['std'])

        # One liner madness from https://stackoverflow.com/a/75056284
        df['rsi'] = 100 - (100 / (1 + df['value']
                                  .diff(1)
                                  .mask(df['value'].diff(1) < 0, 0)
                                  .ewm(alpha=1/self.width, adjust=False).mean() / df['value'].diff(1)
                                  .mask(df['value'].diff(1) > 0, -0.0).abs()
                                  .ewm(alpha=1/self.width, adjust=False).mean()))

        for _, row in df.dropna().iterrows():
            insights = [
                InsightResult(
                    f"Upper BB{self.width}",
                    row['upper'],
                    arrow.get(row['date']),
                    row['symbol']
                ),
                InsightResult(
                    f"Lower BB{self.width}",
                    row['lower'],
                    arrow.get(row['date']),
                    row['symbol']
                ),
                InsightResult(
                    f"SMA{self.width}",
                    row['sma'],
                    arrow.get(row['date']),
                    row['symbol']
                ),
                InsightResult(
                    f"RSI{self.width}",
                    row['rsi'],
                    arrow.get(row['date']),
                    row['symbol']
                )
            ]

            results.extend(insights)

        if self.most_recent:
            return results[-4:]

        return results
