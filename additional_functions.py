import json

import yfinance as yf
from decouple import config
from pandas import DataFrame

proxy_server = config('PROXY_SERVER')

def get_history_df(company_name: str) -> DataFrame:
    ticker = yf.Ticker(company_name)
    history_df = ticker.history(period="max", proxy=proxy_server)
    return history_df


"""
Options orient: 'columns','records','index','split','table'
"""
def df_to_json(df: DataFrame, orient: str = "table") -> json:
    return df.to_json(orient=orient)
