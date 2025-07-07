from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from string import Template
import os

DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')
DB_PORT = os.getenv('DB_PORT')
HOST = os.getenv('ENV')
if not HOST == 'production':
  HOST = 'postgres'

DB_URL = Template('postgresql+psycopg2://$user:$password@$host:$port/easycrit.main')

connString = DB_URL.safe_substitute(user=DB_USER, password=DB_PASSWORD, host=HOST, port=DB_PORT)
engine = create_engine(connString, echo=True)

Session = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

class Base(DeclarativeBase):
  pass

def get_session():
  with Session() as session:
    yield session

def setup_db():
  Base.metadata.create_all(engine)
