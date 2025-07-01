from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from string import Template
import os

DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')
DB_PORT = os.getenv('DB_PORT')
HOST = os.getenv('ENV')
if not HOST == 'production':
    HOST = 'localhost'

DB_URL = Template('postgresql+psycopg2://$user:$password@$host:$port/easycrit')

connString = DB_URL.safe_substitute(user=DB_USER, password=DB_PASSWORD, host=HOST, port=DB_PORT)
engine = create_engine(connString)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def create_tables():
  Base.metadata.create_all(bind=engine)
