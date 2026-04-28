from pydantic import BaseModel, Field

class Shipment(BaseModel):
    weight: float = Field(description="Minimum weight is 0.1 kg & Maximum weight is 25 kg", gt=0.1, le=25)
    content: str = Field(description="Description of the shipment content")
    destination: int | None = Field(description="Destination ID for the shipment", default=None)
    details: str = Field(description="Additional details about the shipment")