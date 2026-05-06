from sqlmodel import Field, SQLModel


class Shipment(SQLModel):
    id: int
    content: str
    weight: float = Field(le=25)
    destination: int
    status: str
    estimated_delivery: str