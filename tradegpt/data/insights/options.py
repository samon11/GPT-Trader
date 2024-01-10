import json
import arrow
import pandas as pd
from typing import List
from data.insights.insight import Insight
from data.models import Contract, InsightResult


class Options(Insight):
    def generate(self, datum: pd.DataFrame) -> List[InsightResult]:
        results = []
        df = datum[datum['name'] == "OPTION"]

        for _, row in df.iterrows():
            contract = json.loads(row['value'])
            results.append(
                InsightResult(
                    "Option",
                    row['value'],
                    arrow.get(row['date']),
                    contract['desc'],
                    prompt_func=self._option_to_prompt
                )
            )

        return results
    
    @staticmethod
    def _option_to_prompt(insight: InsightResult):
        contract: dict = json.loads(insight.value)
        date = insight.date.shift(days=contract['daysToExp']).format("MMM DD")
        prompt = f'{date}: {contract["contractType"]} {contract["strike"]}, '
        ignore_keys = ['daysToExp', 'contractType', 'itm', 'desc']

        for k, v in contract.items():
            if k not in ignore_keys:
                prompt += f'{k} {v}, '

        return prompt
