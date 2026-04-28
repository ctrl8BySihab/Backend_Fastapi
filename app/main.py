from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.schemas import ShipmentStatus, BaseShipment, ShipmentRead, ShipmentUpdate

shipments = {
    12001: {
        "weight": 8.2,
        "content": "aluminum sheets",
        "status": "placed",
        "destination": 11002,
    },
    12002: {
        "weight": 14.7,
        "content": "steel rods",
        "status": "shipped",
        "destination": 11003,
    },
    12003: {
        "weight": 11.4,
        "content": "copper wires",
        "status": "delivered",
        "destination": 11002,
    },
    12004: {
        "weight": 17.8,
        "content": "iron plates",
        "status": "in transit",
        "destination": 11005,
    },
    12005: {
        "weight": 10.3,
        "content": "brass fittings",
        "status": "returned",
        "destination": 11008,
    },
}

app = FastAPI()


@app.get("/shipments", response_model= ShipmentRead)
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipments[id]


@app.post("/shipments", response_model=ShipmentRead)
def submit_shipment(data: BaseShipment):
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **data.model_dump(),
        "status": ShipmentStatus.placed
    }
    return shipments[new_id]|{"details": f"Shipment created with ID {new_id}"}


@app.patch("/shipments", response_model=ShipmentUpdate)
def update_shipment(id: int, data: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments[id] = {
        **data.model_dump(exclude_none=True)
    }
    return shipments[id]


@app.get("/http_docs", include_in_schema=False)
def get_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Shipment API Documentation"
    )