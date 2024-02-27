import requests
import pandas as pd
from fmp_api_key import API_KEY

def get_financial_statement(ticker: str, api_key: str=API_KEY, period: str='annual',
                            balance_sheet: bool=True,
                            income_statement: bool=False,
                            cashflow_statement: bool=False):
    """
    Retrieves statment data from fmp and returns json
    """
    payload = {'period': period, 'apikey': api_key}
    BASE_URL = 'https://financialmodelingprep.com/api/v3/'

    def statement_type(balance: bool= balance_sheet,
                       income: bool= income_statement,
                       cashflow: bool= cashflow_statement) -> str:
        """
        Returns the appropriate string to retrieve the requested statement from fmp
        """
        if balance:
            return 'balance-sheet-statement'
        if income:
            return 'income-statement'
        if cashflow:
            return 'cash-flow-statement'
        return None

    statement = statement_type()

    try:
        url = f'{BASE_URL}{statement}/{ticker}?'
        response = requests.get(url, params=payload, timeout= 5)
        return response.json()
    except Exception as exc:
        print("Unable to retrieve data")
        raise exc

def json_to_dict(data_json) -> dict:
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
                statement_dict[key].append(value)
            elif key not in no_entry:
                statement_dict[key] = [value]
    return statement_dict

# Change data retrieval to an object
# Function for vertical analysis
# Function for horizontal analysis
