from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    category: str | None = None
    cost_price: float = Field(ge=0)
    sale_price: float = Field(ge=0)
    stock_quantity: int = Field(ge=0)
    minimum_stock: int = Field(ge=0)
    description: str | None = None
