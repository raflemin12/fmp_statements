import pandas as pd
from data_retrieval import *

def main():
    response = get_financial_statement('NKE')
    print(response)

if __name__ == '__main__':
    main()
