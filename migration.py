import psycopg2
from decouple import config
from sqlalchemy import create_engine

from models import Base

def create_dbs() -> None:
    database = config('POSTGRES_DB')
    db_user = config('POSTGRES_USER')
    db_password = config('POSTGRES_PASSWORD')
    conn = psycopg2.connect(
       database=database, user=db_user, password=db_password, host='db', port='5432'
    )

    try:
        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute("""CREATE database finance_yahoo""")
        cursor.execute("""CREATE database test_finance_yahoo""")
        print("Databases created successfully!")
    finally:
        # closing the connection
        conn.close()

def migration() -> None:
    engine = create_engine(config('DB_LINK'))
    # create all tables from models
    Base.metadata.create_all(engine)
