import pandas as pd
from data_retrieval import *

def main():
    nke_balance = Balance_sheet('NKE')
    print(nke_balance.statement_data)

if __name__ == '__main__':
    main()
