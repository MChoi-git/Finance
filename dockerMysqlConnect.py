import sqlalchemy as db
import time
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert

#Notes:
#   -Can find the mysql log file in .mysql_history in home dir (doesn't include actions from this file or others)
#   -How do I find the real logs????

#Set config for engine
config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Stanleymug1!',
        'database': 'test'
        }
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

#Create engine
engine = db.create_engine(connection_str)
connection = engine.connect()

#Print columns of all tables
'''
inspector = inspect(engine)

for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column['name'])
'''

#Begin once style
#AKA: BEGIN (implicit) -> Start of DBAPI's implicit transaction
'''
with engine.begin() as conn:
    conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
            )
'''

#Fetching rows
'''
print("Fetching rows:")
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x:{row.x} y: {row.y}")
    #Row objects act like named tuples
    #Refer to sqlalchemy docs for usage details
print('-'*50)

#Sending parameters
print("Sending parameters:")
with engine.connect() as conn:
    result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"),
            {"y": 2}
    )
    for row in result:
        print(f"x: {row.x} y: {row.y}")
print('-'*50)

#Bundling parameters with a statement
print("Bundling parameters with stmt and ORM session intro:")
stmt = text("SELECT x,y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(f"x: {row.x} y: {row.y}")
print('-'*50)
'''

#Working with Database Metadata

#Setting up MetaData with Table Objects
'''
metadata = MetaData()
user_table = Table(
        "user_account",
        metadata,
        Column('id', Integer, primary_key = True),
        Column('name', String(30)),
        Column('fullname', String(30))
)#Columns accessed via array at Table.c

#Declaring simple constraints
address_table = Table(
        "address",
        metadata, 
        Column('id', Integer, primary_key=True),
        Column('user_id', ForeignKey('user_account.id'), nullable=False),
        Column('email_address', String(30), nullable=False)
)

#Emitting Data Definition Language (DDL) to the database
# MetaData -> Tables -> Columns and Constraints: Very important concept!
metadata.create_all(engine)
'''
###########################################################################################
#Defining Table Metadata with the ORM

#Setting up the registry
Base = declarative_base()

#Declaring mapped classes
class User2(Base):
    __tablename__ = 'user_account2'

    id = Column(Integer, primary_key = True)
    name = Column(String(30))
    fullname = Column(String(30))
    
    addresses2 = relationship("Address2", back_populates="user2")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address2(Base):
    __tablename__ = 'address2'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account2.id'))
    
    user2 = relationship("User2", back_populates="addresses2")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

Base.metadata.create_all(engine)
'''
#Data manipulation with ORM
squidward = User(name='squidward', fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
print(squidward)

#Adding objects to sesstion
session = Session(engine)
session.add(squidward)
session.add(krabs)

#Flushing
session.flush()

#Identity map
some_squidward = session.get(User, 3)
print(some_squidward)
print(some_squidward is squidward)
#session.commit()

#Updating ORM objects
#sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
#print(sandy) prints the sandy row
#sandy.fullname = "Sandy Squirrel"
#sandy in session.dirty (True)
'''

