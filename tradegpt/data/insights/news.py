import arrow
import pandas as pd
from typing import List
from data.insights.insight import Insight
from data.models import InsightResult


class News(Insight):
    def __init__(self) -> None:
        super().__init__(f"News")

    def generate(self, datum: pd.DataFrame) -> List[InsightResult]:
        results = []
        df = datum[datum['name'] == "NEWS"]

        for _, row in df.dropna().iterrows():
            results.append(
                InsightResult(
                    "News",
                    row['value'],
                    arrow.get(row['date']),
                    row['symbol']
                )
            )

        return results
