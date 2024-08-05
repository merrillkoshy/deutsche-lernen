from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import SECRET_KEY, SQLALCHEMY_DATABASE_URL, Settings

settings = Settings(
    SQLALCHEMY_DATABASE_URL=SQLALCHEMY_DATABASE_URL or "", SECRET_KEY=SECRET_KEY or ""
)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
