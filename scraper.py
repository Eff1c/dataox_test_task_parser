import yfinance as yf
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company

proxy_server = config('PROXY_SERVER')

engine = create_engine(config('DB_LINK'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def parse(tickers_names: str) -> None:
    tickers = yf.Tickers(tickers_names)

    for ticker_name, ticker in zip(tickers.tickers, tickers.tickers.values()):
        history_df = ticker.history(period="max", proxy=proxy_server)

        # get id company and append in this column
        company_id = Company.add_new_company(ticker_name, session)
        history_df["company_id"] = company_id

        # save dataframe to database
        history_df.to_sql('history', engine, if_exists="append")
