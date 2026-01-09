from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgresql+psycopg2://postgres:root1234@localhost:5432/taxi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)