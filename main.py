import pandas as pd
from data_retrieval import *

def main():
    response = get_financial_statement('NKE')
    d = json_to_dict(response)
    print(horizontal_analysis(d))

if __name__ == '__main__':
    main()
