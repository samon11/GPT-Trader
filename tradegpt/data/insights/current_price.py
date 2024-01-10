import arrow
import pandas as pd
from typing import List

from pandas import DataFrame
from data.insights.insight import Insight
from data.models import InsightResult

class CurrentPrice(Insight):
    def __init__(self) -> None:
        super().__init__("Current Price")

    def generate(self, datum: DataFrame) -> List[InsightResult]:
        data = datum[datum['name'] == 'PRICE'].reset_index()

        return [
            InsightResult(
                'Price',
                data.at[0, 'value'],
                data.at[0, 'date'],
                data.at[0, 'symbol']
            )
        ]
