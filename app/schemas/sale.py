from pydantic import BaseModel, Field


class SaleItemInput(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    customer_name: str | None = None
    payment_method: str
    notes: str | None = None
    items: list[SaleItemInput]
