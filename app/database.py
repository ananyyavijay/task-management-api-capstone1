import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
 
from sqlalchemy import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

id_type = UUID().with_variant(UNIQUEIDENTIFIER, "mssql")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./capstone.db"   # local fallback
)

# SQLite needs check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
 
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()