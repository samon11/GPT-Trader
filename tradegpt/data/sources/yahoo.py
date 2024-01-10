from typing import List
import yfinance as yf
from arrow import Arrow
import arrow
from data.models import Datum
from data.sources.datasource import DataSource


class YahooSource(DataSource):
    """
    A data source that fetches financial data from Yahoo Finance API.

    Methods:
        fetch_data(start: Arrow, end: Arrow, symbol: str) -> List[Datum]:
            Fetches financial data for a given symbol between two dates.
        _get_vix(symbol) -> Datum:
            Fetches the current value of VIX index.
    """

    def fetch_data(self, start: Arrow, end: Arrow, symbol: str) -> List[Datum]:
        """
        Fetches financial data for a given symbol between two dates.

        Args:
            start (Arrow): The start date of the data.
            end (Arrow): The end date of the data.
            symbol (str): The symbol of the stock.

        Returns:
            List[Datum]: A list of Datum objects containing the financial data.
        """
        ticker = yf.Ticker(symbol)

        history = ticker.history(start=start.datetime, end=end.datetime)
        today_news = [n['title'] for n in ticker.news]

        results = []
        for date, row in history.iterrows():
            open = Datum('OPEN', arrow.get(date), row['Open'], symbol)
            high = Datum('HIGH', arrow.get(date), row['High'], symbol)
            low = Datum('LOW', arrow.get(date), row['Low'], symbol)
            close = Datum('CLOSE', arrow.get(date), row['Close'], symbol)
            volume = Datum('VOLUME', arrow.get(date), row['Volume'], symbol)

            results.extend([open, high, low, close, volume])

        for title in today_news:
            results.append(Datum('NEWS', arrow.now(tz='America/New_York'), title, symbol))

        current_price = (ticker.info['bid'] + ticker.info['ask']) / 2
        results.append(
            Datum('PRICE', arrow.now(tz='America/New_York'), current_price, symbol)
        )

        results.extend(self._get_vix(symbol))

        return results
    
    def _get_vix(self, symbol, days=7) -> List[Datum]:
        """
        Fetches the current value of VIX index.

        Args:
            symbol (str): The symbol of the stock.

        Returns:
            Datum: A Datum object containing the current value of VIX index.
        """
        vix = yf.Ticker('^VIX')
        history = vix.history()
        results = []
        
        data = history.iloc[-days:]

        for date, row in data.iterrows():
            results.append(Datum('VIX', arrow.get(date), round(row['Close'], 2), symbol))

        return results
