from sqlalchemy import create_engine
from sqlmodel import SQLModel

# Create the database engine connected to sqlite.db
engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,                              # Logs all SQL statements
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Import models so SQLModel.metadata is aware of all tables
from app.database.model import Shipment

# Create all tables defined in SQLModel models if they don't exist
SQLModel.metadata.create_all(bind=engine)