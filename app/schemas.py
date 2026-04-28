from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class BaseShipment(BaseModel):
    weight: float = Field(
        description="Weight of the shipment in kilograms", gt=0, le=25
    )
    content: str = Field(description="Description of the shipment content")
    destination: int = Field(description="ID of the destination location")


class ShipmentRead(BaseShipment):
    status: ShipmentStatus = Field(description="Current status of the shipment")


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    weight: float | None = Field(
        description="Weight of the shipment in kilograms", gt=0, le=25, default=None
    )
    content: str | None = Field(description="Description of the shipment content", default=None)
    destination: int | None = Field(description="ID of the destination location", default=None)
    status: ShipmentStatus = Field(description="Current status of the shipment")