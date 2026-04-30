from pydantic import BaseModel, Field
from enum import Enum


# Possible lifecycle states of a shipment
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# Shared fields used across create and read schemas
class BaseShipment(BaseModel):
    weight: float = Field(
        description="Weight of the shipment in kilograms", gt=0, le=25
    )
    content: str = Field(description="Description of the shipment content")
    destination: int = Field(description="ID of the destination location")


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
    destination: int | None = Field(description="ID of the destination location", default=None)
    status: ShipmentStatus = Field(description="Current status of the shipment")