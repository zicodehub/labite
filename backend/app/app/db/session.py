from typing import Generator
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size = 100, max_overflow=200)

orm.configure_mappers() 

def SessionLocal():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

def get_db() -> Generator:
    try:
        print("Calling SessionLocal")
        db = SessionLocal()
        yield db
    finally:
        print("out")
        db.close()