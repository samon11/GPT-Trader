from typing import List
from arrow import Arrow
import os
import json
import arrow
import pandas as pd

from data.sources.datasource import DataSource
from data.insights.insight import Insight
from data.models import Datum, InsightResult
from utils import PROJECT_ROOT


class DataContext:
    def __init__(self, sources: List[DataSource] = [], cache=True) -> None:
        self.sources = sources
        self.cache = cache

    def register(self, source: DataSource):
        self.sources.append(source)

    def fetch_all(self, start: Arrow, end: Arrow, symbols):
        datum = []

        existing = self._get_save_path(start)
        if os.path.exists(existing) and self.cache:
            with open(existing, 'r') as f:
                content = json.load(f)
                return [Datum.from_dict(d) for d in content]

        for source in self.sources:
            for symbol in symbols:
                datum.extend(source.fetch_data(start, end, symbol))

        self._save(start, datum)

        return datum
    
    def _save(self, start: Arrow, datum: List[Datum]):
        path = self._get_save_path(start)
        dir = os.path.dirname(path)

        if not os.path.exists(dir):
            os.makedirs(path)

        if not os.path.exists(path):
            with open(path, 'w') as f:
                content = [d.to_dict() for d in datum]
                json.dump(content, f)

    def _get_save_path(self, start: Arrow):
        return os.path.join(PROJECT_ROOT, "cache", start.strftime('%Y-%m-%d') + '.json')

class InsightContext:
    def __init__(self, data: DataContext, symbols: list, insights=[]) -> None:
        self.insights: List[Insight] = insights
        self.data_context = data
        self.symbols = symbols

    def register(self, insight: Insight):
        self.insights.append(insight)

    def _get_lookback(self, start: Arrow):
        max_lookback = max([i.day_lookback for i in self.insights])
        return start.shift(days=-max_lookback)

    def get_insights(self, start: Arrow, end: Arrow = arrow.now(tz="America/New_York")) -> List[InsightResult]:
        lookback_start = self._get_lookback(start)

        datum = self.data_context.fetch_all(lookback_start, end, self.symbols)
        results = []

        for symbol in self.symbols:
            for insight in self.insights:
                symbol_datum = pd.DataFrame.from_records([d.to_dict() for d in datum if d.symbol == symbol])
                if not symbol_datum.empty:
                    results.extend(insight.generate(symbol_datum))

        # handle None symbols
        for insight in self.insights:
            none_datum = pd.DataFrame.from_records([d.to_dict() for d in datum if d.symbol == None])
            if not none_datum.empty:
                results.extend(insight.generate(none_datum))

        return results
