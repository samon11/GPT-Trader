from typing import List
from pandas import DataFrame
from data.models import InsightResult

class Insight:
    def __init__(self, name: str = 'Insight', day_lookback=1) -> None:
        self.name = name
        self.day_lookback = day_lookback

    def generate(self, datum: DataFrame) -> List[InsightResult]:
        raise NotImplementedError()