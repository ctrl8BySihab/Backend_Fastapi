from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.database.model import Shipment

# Create the database engine connected to sqlite.db
engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,                              # Logs all SQL statements
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Create a method to use this task from another module
def create_table():
    # Import models so SQLModel.metadata is aware of all tables
    SQLModel.metadata.create_all(bind=engine)

# Get a fresh session for each endpoint request
def get_session():
    with Session(bind=engine) as session:
        yield session

# Create Annotated type session dependency
SessionDep = Annotated[Session, Depends(get_session)]