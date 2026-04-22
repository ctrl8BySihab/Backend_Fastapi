from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()

db = {
    12001: {
        "weight": 0.6,
        "content": "Glassware",
        "status": "In-Transit"
    },
    12002: {
        "weight": 0.5,
        "content": "Books",
        "status": "Pending"
    },
    12003: {
        "weight": 3.0,
        "content": "Furniture",
        "status": "In-Transit"
    },
    12004: {
        "weight": 0.2,
        "content": "Clothing",
        "status": "Delivered"
    },
    12005: {
        "weight": 1.5,
        "content": "Tools",
        "status": "Available"
    },
    12006: {
        "weight": 0.8,
        "content": "Toys",
        "status": "In-Transit"
    },
    12007: {
        "weight": 2.5,
        "content": "Appliances",
        "status": "Pending"
    }
}

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    latest_id = max(db.keys())
    return {"id": latest_id} | db[latest_id]

@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]: 
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide an ID to fetch the shipment details!"
        )
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given ID {id} does not exist in the database!"
        )
    return {"id": id} | db[id]

@app.post("/shipment")
def submit_shipment(weight: float | None = None, content: str | None = None) -> dict[str, Any]:
    if weight is None or content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide both weight and content to submit a shipment!"
        )
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight is 25kg!"
        )
    new_id = max(db.keys()) + 1
    db[new_id] = {
        "weight": weight,
        "content": content,
        "status": "Placed"
    }
    return {"id": new_id} | db[new_id]

@app.post("/shipment/body")
def submit_shipment_body(data: dict[str, Any]) -> dict[str, Any]:
    weight = data["weight"]
    content = data["content"]
    new_id = max(db.keys()) + 1
    db[new_id] = {
        "weight": weight,
        "content": content,
        "status": "Placed"
    }
    return {"id": new_id} | db[new_id]

@app.get("/shipment/{field}")
def shipment_field(field: str, id: int) -> dict[str, Any]:
    return {
        field: db[id][field]
    }

@app.get("/http_docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url= app.openapi_url, title="Scalar API Reference")