from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from string import Template
import os

DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
HOST = os.getenv('ENV')
if not HOST == 'production':
  HOST = 'postgres'

DB_URL = Template('postgresql+psycopg2://$user:$password@$host:$port/$db_name')

connString = DB_URL.safe_substitute(user=DB_USER, password=DB_PASSWORD, host=HOST, port=DB_PORT, db_name=DB_NAME)
engine = create_engine(connString, echo=True)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)


class Base(DeclarativeBase):
  pass


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def create_tables():
  Base.metadata.create_all(bind=engine)