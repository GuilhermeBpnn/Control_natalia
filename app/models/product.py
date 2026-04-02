from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(80), unique=True, nullable=False, index=True)
    category = Column(String(80), nullable=True)
    cost_price = Column(Float, nullable=False, default=0)
    sale_price = Column(Float, nullable=False, default=0)
    stock_quantity = Column(Integer, nullable=False, default=0)
    minimum_stock = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sale_items = relationship('SaleItem', back_populates='product')
    stock_movements = relationship('StockMovement', back_populates='product')
