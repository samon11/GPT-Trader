import arrow
import pandas as pd
from typing import List

from pandas import DataFrame
from data.insights.insight import Insight
from data.models import InsightResult

class VIX(Insight):
    def generate(self, datum: DataFrame) -> List[InsightResult]:
        data = datum[datum['name'] == 'VIX'].reset_index()
        results = []
        if not data.empty:
            for i, row in data.iterrows():
                results.append(
                    InsightResult(
                        'VIX',
                        row['value'],
                        arrow.get(row['date']),
                        None
                    )
                )
        
        return results
