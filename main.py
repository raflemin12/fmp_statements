import pandas as pd
from data_retrieval import *

def main():
    nke_balance = BalanceSheet('NKE')
    print(nke_balance.statement_data)

if __name__ == '__main__':
    main()
