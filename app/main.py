from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import col, select

from app.database.model import Shipment
from app.database.session import SessionDep, create_table
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


# Add context manager
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_table()
    yield


app = FastAPI(lifespan=lifespan_handler)


# Returns the shipment with the highest ID
@app.get("/shipments/latest", response_model=None)
def get_latest_shipment(session: SessionDep):
    shipment = session.exec(select(Shipment).order_by(col(Shipment.id).desc())).first()
    return shipment


# Returns a single shipment by ID
@app.get("/shipments", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


# Creates a new shipment with status "placed" and persists to JSON
@app.post("/shipments", response_model=None)
def submit_shipment(data: ShipmentCreate, session: SessionDep):
    shipment = Shipment(
        **data.model_dump(),
        status="placed",
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return {"details": f"Shipment with ID #{shipment.id} has been submitted"}


# Partially updates a shipment; only provided fields are changed
@app.patch("/shipments", response_model=None)
def update_shipment(id: int, data: ShipmentUpdate, session: SessionDep):
    update_shipment = data.model_dump(exclude_none=True)
    if not update_shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipment.sqlmodel_update(update_shipment)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


# Removes a shipment from the store and persists the change
@app.delete("/shipments", response_model=None)
def delete_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    session.delete(shipment)
    session.commit()
    return {"details": f"Shipment with ID #{id} has been deleted"}


# Endpoint to serve the API documentation as a scalar reference
@app.get("/http_docs", include_in_schema=False)
def get_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title="Shipment API Documentation"
    )
