from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Azure SQL Database connection string format
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://azureuser:e28haY-D#HrAd_r@flow-task-sqlserver.database.windows.net:1433/flow-task-adb?driver=ODBC+Driver+18+for+SQL+Server",
)


# Create engine with Azure SQL specific settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"TrustServerCertificate": "yes"},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
