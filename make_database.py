#Import 
import sqlalchemy as db
import time
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Date
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

    def __repr__(self):
        return f"Primary(id={self.id!r}, name={self.name!r}, ticker={self.ticker!r})"

#Create class for open/high/low/close data
class OHLC(Base):
    __tablename__ = 'ohlc'
    
    #Columns definition
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    dayopen = Column(Integer, nullable=False)
    dayhigh= Column(Integer, nullable=False)
    daylow = Column(Integer, nullable=False)
    dayclose = Column(Integer, nullable=False)
    dayvolume = Column(Integer, nullable=False)

    primary = relationship("PrimaryDB", back_populates="ohlc")

#Create class for financials TBD

Base.metadata.create_all(engine)
