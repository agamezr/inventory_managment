import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)

meta = MetaData()
conn = engine.connect()
Base = declarative_base()