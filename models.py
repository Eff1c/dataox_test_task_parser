from __future__ import annotations

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.orm.session import Session

from custom_exceptions import ObjectIsExist

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name

    @classmethod
    def get_company(
        cls,
        name: str,
        session: Session
    ) -> Company:
        company = session.query(
            cls
        ).filter(
            cls.name == name
        ).one_or_none()
        """one_or_none() rather than first() because 
        field "word" is unique and shouldn't have many results"""

        return company

    @classmethod
    def add_new_company(
        cls,
        name: str,
        session: Session
    ) -> int:
        if cls.get_company(name, session) is not None:
            raise ObjectIsExist

        company = cls(
            name=name
        )
        session.add(company)
        session.commit()

        return company.id


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    date = Column("Date", DateTime(timezone=False))
    open = Column("Open", Float(53))
    high = Column("High", Float(53))
    low = Column("Low", Float(53))
    close = Column("Close", Float(53))
    volume = Column("Volume", Integer)
    dividends = Column("Dividends", Integer)
    stock_splits = Column("Stock Splits", Integer)
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", backref=backref("history"))
