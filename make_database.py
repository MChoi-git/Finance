#Creates primary, ohlc, and financials databases in docker container

#Import 
import sqlalchemy as db
import time
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert

#Set config for connection to docker
config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Stanleymug1!',
        'database': 'securities'
        }
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

engine = db.create_engine(connection_str)
connection = engine.connect()

Base = declarative_base()

#Create class for primary securities table
class PrimaryDB(Base):
    __tablename__ = 'primarydb'

    #Columns definition
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ticker = Column(String(8))

    ohlc = relationship("OHLC", back_populates="primarydb")
    financials = relationship("Financials", back_populates="primarydb")

    def __repr__(self):
        return f"Primary(id={self.id!r}, name={self.name!r}, ticker={self.ticker!r})"

#Create class for open/high/low/close data
class OHLC(Base):
    __tablename__ = 'ohlc'
    
    #Columns definition
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    dayopen = Column(Integer, nullable=False)
    dayhigh= Column(Integer, nullable=False)
    daylow = Column(Integer, nullable=False)
    dayclose = Column(Integer, nullable=False)
    dayvolume = Column(Integer, nullable=False)

    primary = relationship("PrimaryDB", back_populates="ohlc")

    def __repr__(self):
        return f"OHLC(id={self.id!r}, date={self.date!r}, dayopen={self.dayopen!r}, dayhigh={self.dayhigh!r}, daylow={self.daylow!r}, dayclose={self.dayclose!r}, dayvolume={self.dayvolume!r})"

#Create class for financials TBD
class Financials(Base):
    __tablename__ = 'financials'

    #Columns definition
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    debt_to_equity_ratio = Column(Float)
    dividend_yield = Column(Float)
    earnings_per_diluted_share = Column(Float)
    gross_profit = Column(Integer)
    net_income = Column(Integer)
    price_to_earnings_ratio = Column(Float)
    revenues_usd = Column(Integer)

    primary = relationship("PrimaryDB", back_populates="financials")

    def __repr__(self):
        return f"Financials(id={self.id!r}, date={self.date!r}, debt_to_equity_ratio={self.debt_to_equity_ratio!r}, dividend_yield={self.dividend_yield!r}, earnings_per_diluted_share={self.earnings_per_diluted_share!r}, gross_profit={self.gross_profit!r}, net_income={self.net_income!r}, price_to_earnings_ratio={self.price_to_earnings_ratio!r}, revenues_usd={self.revenues_usd!r})"


Base.metadata.create_all(engine)
