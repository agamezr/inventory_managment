from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, Enum
from app.config.database import meta, engine, Base
from sqlalchemy.orm import relationship

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'), nullable=False)
    store_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)

    product = relationship("Product", back_populates="inventories")