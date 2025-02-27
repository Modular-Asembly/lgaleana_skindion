import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

# Load the database URL from the environment variable
db_url = os.getenv("DB_URL")
if not db_url:
    raise EnvironmentError("Environment variable DB_URL is not set.")
DB_URL: str = db_url

# Create the SQLAlchemy engine
engine = create_engine(DB_URL, future=True)

# Define the base class for declarative models
class Base(DeclarativeBase):
    pass

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_session() -> Generator[Session, None, None]:
    """
    Returns a SQLAlchemy session. This function should be used as a FastAPI dependency.
    """
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
