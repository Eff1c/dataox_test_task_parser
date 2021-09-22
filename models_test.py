import datetime

import pytest
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from models import Base, Company, History

def create_test_data(db_session: Session):
    test_item = Company(
        name="test"
    )

    db_session.add(test_item)
    db_session.commit()


@pytest.fixture(scope="session")
def db_session():
    engine = create_engine(config('TEST_DB_LINK'))
    # create all tables from models
    Base.metadata.create_all(engine)
    # create session
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    try:
        create_test_data(session)

        yield session

    finally:
        session.close()
        # remove all tables
        Base.metadata.drop_all(bind=engine)


def test_get_company(
    db_session: Session
):
    assert Company.get_company("test", db_session) is not None


def test_add_new_company(
    db_session: Session
):
    assert Company.add_new_company("dataox", db_session) is not None


def test_create_history(
    db_session: Session
):
    test_company = Company.get_company("test", db_session)
    new_history = History(
        date=datetime.datetime.today(),
        open=300.0,
        high=400.0,
        low=200.0,
        close=350.0,
        volume=300,
        dividends=0,
        stock_splits=0,
        company=test_company
    )

    db_session.add(new_history)
    db_session.commit()
