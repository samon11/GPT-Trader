import dataclasses
import os
import arrow
from dotenv import load_dotenv
from arrow import Arrow
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
import tda
import json
import atexit
from selenium.webdriver.chrome.service import Service as ChromeService

from data.sources.datasource import DataSource
from data.models import Contract, Datum

load_dotenv()

API_KEY = os.getenv('API_KEY')
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_PATH = os.getenv('TOKEN_PATH')

class TDAmeritrade(DataSource):
    def __init__(self, max_dte=36) -> None:
        self.max_dte = max_dte
        self.client = tda.auth.easy_client(
            API_KEY,
            REDIRECT_URI,
            TOKEN_PATH,
            self._make_webdriver
        )

    def fetch_data(self, start: Arrow, end: Arrow, symbol: str):
        now = arrow.now(tz="America/New_York")
        response = self.client.get_option_chain(
            symbol,
            contract_type=self.client.Options.ContractType.ALL, 
            from_date=now.shift(days=30).datetime, 
            to_date=now.shift(days=self.max_dte).datetime,
            strike_count=20,
            strike_range=self.client.Options.StrikeRange.ALL)
        
        results = self._parse_chain(response.json())
        return results
    
    @staticmethod
    def _parse_chain(response):
        contracts = []

        maps = []
        maps.extend(response['callExpDateMap'].values())
        maps.extend(response['putExpDateMap'].values())
        
        for date in maps:
            for strike in date.values():
                contract = Contract(
                    desc=strike[0]['symbol'],
                    strike=strike[0]["strikePrice"],
                    delta=strike[0]["delta"],
                    theta=strike[0]["theta"],
                    gamma=strike[0]["gamma"],
                    vega=strike[0]["vega"],
                    rho=strike[0]["rho"],
                    bid=strike[0]["bid"],
                    ask=strike[0]["ask"],
                    volume=strike[0]["totalVolume"],
                    openInterest=strike[0]["openInterest"],
                    volatility=strike[0]["volatility"],
                    daysToExp=strike[0]["daysToExpiration"],
                    contractType=strike[0]["putCall"],
                    itm=strike[0]["inTheMoney"])
                
                value = json.dumps(dataclasses.asdict(contract))
                contracts.append(Datum(
                    name='OPTION',
                    date=arrow.now(tz='America/New_York'),
                    value=value,
                    symbol=contract.desc.split('_')[0]
                ))

        return contracts

    @staticmethod
    def _make_webdriver():
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 
        driver.implicitly_wait(5)
        atexit.register(lambda: driver.quit())
        return driver