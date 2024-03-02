import requests
import pandas as pd
from fmp_api_key import API_KEY

class Statement:
    def __init__(self, ticker: str, period: str='annual') -> None:
        self.ticker = ticker
        self.BASE_URL = 'https://financialmodelingprep.com/api/v3/'
        self.__api_key = API_KEY
        self.period = period
        self.payload = {'period': self.period, 'apikey': self.__api_key}

    def get_financial_statement_json(self, statement:str):
        """
        Retrieves statment data from fmp and returns json
        """
        try:
            url = f'{self.BASE_URL}{statement}/{self.ticker}?'
            response = requests.get(url, params=self.payload, timeout= 5)
            return response.json()
        except Exception as exc:
            print("Unable to retrieve data")
            raise exc

    def json_to_dict(self, data_json) -> dict:
        """
        Transforms json data into a dict with datapoint name as the key
        and the datapoint in a list for the dict value
        """
        statement_dict = {}
        no_entry = ['symbol', 'cik', 'fillingDate', 'acceptedDate',
                    'calendarYear', 'period', 'link', 'finalLink', 'reportedCurrency']
        for json in data_json:
            for key, value in json.items():
                if key in statement_dict:
                    statement_dict[key].insert(0,value)
                elif key not in no_entry:
                    statement_dict[key] = [value]
        return statement_dict

    def horizontal_analysis(self, statement_dict:dict) -> dict:
        """
        Takes in the statement_dict from json_to_dict and returns
        horizontal analysis in the same format
        """
        def percent_delta(new:float, old:float) -> float:
            """
            Returns the percentage change from two values
            """
            if old > 0:
                return round((new - old) / old, 3)
        horizon_dict = {}
        for key, lst in statement_dict.items():
            if key == 'date':
                horizon_dict[key] = lst.copy()
            else:
                horizon_dict[key] = [percent_delta(lst[idx], lst[idx-1]) for idx in range(1, len(lst))]
                horizon_dict[key].insert(0,0)
        return horizon_dict

    def vert_analysis(self, statement_dict: dict) -> dict:
        """
        Performs vertical analysis on the given statement.
        Returns the analysis in dict form
        """
        vert_dict = {}
        for key, lst in statement_dict.items():
            if key == 'date':
                vert_dict[key] = lst.copy()
            else:
                vert_dict[key] = [round(lst[idx] / statement_dict['totalAssets'][idx], 3)
                                for idx in range(len(lst))]
        return vert_dict

# Change data retrieval to an object
    # Statement Class
        # Properties:
            # BASE_URL
            # API_KEY
            # ticker
            # period
            # payload
        # Methods:
            # request_json
            # json_to_dict
        # Child Classes:
            # Balance Sheet
            # Income Statement
            # Cashflow Statement
class BalanceSheet(Statement):
    def __init__(self, ticker: str, period: str= 'annual') -> None:
        super().__init__(ticker, period)
        self.statementName = 'balance-sheet-statement'
        self.statement_json = self.get_financial_statement_json(self.statementName)
        self.statement_data = self.json_to_dict(self.statement_json)

class IncomeStatement(Statement):
    def __init__(self, ticker: str, period:str = 'annual') -> None:
        super().__init__(ticker, period)
        self.statementName = 'income-statement'
        self.statement_json = self.get_financial_statement_json(self.statementName)
        self.statement_data = self.json_to_dict(self.statement_json)
