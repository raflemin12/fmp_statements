import pandas as pd
from data_retrieval import *

def main():
    nke_balance = BalanceSheet('NKE')
    nke_balance.remove_date_index(nke_balance.statement_df)
    print(nke_balance.statement_df)

if __name__ == '__main__':
    main()
