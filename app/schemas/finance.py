from pydantic import BaseModel, Field


class FinancialEntryCreate(BaseModel):
    type: str
    category: str
    amount: float = Field(gt=0)
    description: str | None = None
    origin: str | None = None
