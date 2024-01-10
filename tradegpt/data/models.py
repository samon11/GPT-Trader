from dataclasses import dataclass
from typing import Callable
from arrow import Arrow
import arrow

class Datum:
    def __init__(self, name: str, date: Arrow, value, symbol: str) -> None:
        self.name = name
        self.date = date
        self.value = value
        self.symbol = symbol

    def to_dict(self):
        return {
            "name": self.name,
            "date": str(self.date),
            "value": self.value,
            "symbol": self.symbol
        }
    
    @staticmethod
    def from_dict(dict):
        return Datum(dict['name'], arrow.get(dict['date']), dict['value'], dict['symbol'])

class InsightResult:
    def __init__(self, 
                 name: str, 
                 value: str, 
                 date: Arrow, 
                 symbol: str = None, 
                 prompt_func: Callable[[object], str] = None) -> None:
        self.name = name
        self.value = value
        self.date = date
        self.symbol = symbol
        self.prompt_func = prompt_func

    @property
    def id(self):
        return f'{self.name}-{self.symbol}'

    def to_prompt(self):
        if self.prompt_func:
            return self.prompt_func(self)

        if self.symbol is not None and self.symbol.upper() != "N/A":
            if isinstance(self.value, float):
                self.value = round(self.value, 2)

            return f"{self.name} of {self.symbol} is {self.value} on {self.date.format('MMM DD HH:mm')}"

        return f"{self.name} is {self.value} on {self.date.format('MMM DD HH:mm')}"
    
@dataclass
class Contract:
    desc: str
    strike: float
    delta: float
    theta: float
    gamma: float
    vega: float
    rho: float
    volatility: float
    volume: int
    openInterest: int
    bid: float
    ask: float
    daysToExp: int
    contractType: str
    itm: bool
