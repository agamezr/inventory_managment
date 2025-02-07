from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, Enum
from datetime import datetime
from app.config.database import meta, engine, Base


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'), nullable=False)
    store_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)