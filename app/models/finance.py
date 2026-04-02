from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from app.database import Base


class FinancialEntry(Base):
    __tablename__ = 'financial_entries'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)  # income, expense
    category = Column(String(80), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    origin = Column(String(120), nullable=True)
    reference_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
