from sqlalchemy import Column, String, DECIMAL, Index
from app.config.database import Base
from sqlalchemy.orm import relationship
from app.models.inventory import Inventory 
from app.models.movement import Movement

class Product(Base):
    __tablename__ = 'products'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    sku = Column(String, unique=True, nullable=False)

    __table_args__ = (
        Index("idx_product_category", "category"),
    )

    inventories = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    movements = relationship("Movement", back_populates="product", cascade="all, delete-orphan")