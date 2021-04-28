import sqlalchemy as db
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.orm import Session

#Notes:
#   -Can find the mysql log file in .mysql_history in home dir (doesn't include actions from this file or others)
#   -How do I find the real logs????

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

