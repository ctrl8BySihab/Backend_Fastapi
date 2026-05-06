from pydantic import BaseModel, Field
from enum import Enum
from app.database.model import ShipmentStatus

# Shared fields used across create and read schemas
class BaseShipment(BaseModel):
    weight: float = Field(
        description="Weight of the shipment in kilograms", gt=0, le=25
    )
    content: str = Field(description="Description of the shipment content")
    destination: str | None = Field(description="Description of the shipment location", default=None)


# Schema for reading/returning a shipment (includes status)
class ShipmentRead(BaseShipment):
    status: ShipmentStatus = Field(description="Current status of the shipment")


# Schema for creating a shipment (status is auto-set to "placed")
class ShipmentCreate(BaseShipment):
    pass


# Schema for partial updates; all fields are optional except status
class ShipmentUpdate(BaseModel):
    weight: float | None = Field(
        description="Weight of the shipment in kilograms", gt=0, le=25, default=None
    )
    content: str | None = Field(description="Description of the shipment content", default=None)
    status: ShipmentStatus = Field(description="Current status of the shipment", default=ShipmentStatus.placed)
    destination: str | None= Field(description="Description of the shipment location", default=None)