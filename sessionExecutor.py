import sqlalchemy as db
import time
import sys
from sqlalchemy import *
from sqlalchemy.orm import *

#This file is called from transaction window to execute sql db session commands

def transactionExec(args):

    config = {
            'host':'localhost',
            'port':3306,
            'user':'root',
            'password':'tuna123',
            'database':'securities'
            }
    db_user = config.get('user')
    db_pwd = config.get('password')
    db_host = config.get('host')
    db_port = config.get('port')
    db_name = config.get('database')

    connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

    engine = create_engine(connection_str)
    connection = engine.connect()

    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    
    print(f'{args[0]} operation selected. Parameters are: ')
    for item in args[1:]:
        print(item.get())
