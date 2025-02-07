from sqlalchemy.orm import sessionmaker
from app.config.database import engine
from fastapi import Depends
from sqlalchemy.orm import Session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
