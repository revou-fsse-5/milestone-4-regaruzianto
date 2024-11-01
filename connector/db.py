from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#loclhostDB
DB_USERNAME = os.environ.get('DATABASE_USERNAME')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DB_HOST = os.environ.get('DATABASE_HOST')
DB_PORT = os.environ.get('DATABASE_PORT')
DB_NAME = os.environ.get('DATABASE_NAME')

#railwayDB
DBR_USERNAME = os.environ.get('DBR_USERNAME')
DBR_PASSWORD = os.environ.get('DBR_PASSWORD')
DBR_HOST = os.environ.get('DBR_HOST')
DBR_PORT = os.environ.get('DBR_PORT')
DBR_NAME = os.environ.get('DBR_NAME')



Base = declarative_base()

print('connecting to database..')
# engine = create_engine(f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)

engine = create_engine(f'mysql+mysqlconnector://{DBR_USERNAME}:{DBR_PASSWORD}@{DBR_HOST}:{DBR_PORT}/{DBR_NAME}', echo=True)

connection = engine.connect()
print(DB_NAME)
print("Connected to database")

Session = sessionmaker(connection)