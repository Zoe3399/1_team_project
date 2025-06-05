# db.py
from sqlalchemy import create_engine

DB_URI = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DB_URI, echo=False)