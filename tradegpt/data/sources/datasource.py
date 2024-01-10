from abc import ABC, abstractmethod
from typing import List
from arrow import Arrow

from data.models import Datum

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self, start: Arrow, end: Arrow, symbol: str) -> List[Datum]:
        pass