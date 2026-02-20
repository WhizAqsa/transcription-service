from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Database URL
DATABASE_URL = "postgresql://postgres:postgres@db:5433/transcription"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()