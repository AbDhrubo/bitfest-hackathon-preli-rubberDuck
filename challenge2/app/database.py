from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # This creates a SQLite file named 'test.db'

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for models
Base = declarative_base()

from sqlalchemy.orm import Session
from app.database import SessionLocal

# Dependency to create a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

