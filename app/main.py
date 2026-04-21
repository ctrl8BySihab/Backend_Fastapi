from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()

db = {
    12001: {
        "Weight": "600gm",
        "content": "Glassware",
        "status": "In-Transit"
    },
    12002: {
        "Weight": "500gm",
        "content": "Books",
        "status": "Pending"
    },
    12003: {
        "Weight": "3kg",
        "content": "Furniture",
        "status": "In-Transit"
    },
    12004: {
        "Weight": "200gm",
        "content": "Clothing",
        "status": "Delivered"
    },
    12005: {
        "Weight": "1.5kg",
        "content": "Tools",
        "status": "Available"
    },
    12006: {
        "Weight": "800gm",
        "content": "Toys",
        "status": "In-Transit"
    },
    12007: {
        "Weight": "2.5kg",
        "content": "Appliances",
        "status": "Pending"
    }
}

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    latest_id = max(db.keys())
    return {"id": latest_id} | db[latest_id]

@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]: 
    if id not in db:
        return {"Details": "Given ID does not exist in the database!"}
    return {"id": id} | db[id]

@app.get("/http_docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url= app.openapi_url, title="Scalar API Reference")