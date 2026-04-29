from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.schemas import ShipmentStatus, BaseShipment, ShipmentRead, ShipmentCreate, ShipmentUpdate
from app.database import shipments, save

app = FastAPI()


@app.get("/shipments/latest", response_model=None)
def get_latest_shipment():
    id = max(shipments.keys())
    return {"id": id} | shipments[id]


@app.get("/shipments", response_model= ShipmentRead)
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipments[id]


@app.post("/shipments", response_model=None)
def submit_shipment(data: ShipmentCreate):
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "id": new_id,
        **data.model_dump(),
        "status": ShipmentStatus.placed
    }
    save()
    return {"details": f"Shipment with ID #{new_id} has been submitted", "id": new_id} | shipments[new_id]


@app.patch("/shipments", response_model=None)
def update_shipment(id: int, data: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments[id].update(**data.model_dump(exclude_none=True))
    save()
    return shipments[id]


@app.delete("/shipments", response_model=None)
def delete_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments.pop(id)
    return {
        "details": f"Shipment with ID #{id} has been deleted"
    }


@app.get("/http_docs", include_in_schema=False)
def get_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Shipment API Documentation"
    )