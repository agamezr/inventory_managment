from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, Enum
from datetime import datetime
from app.config.database import meta, engine, Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    sku = Column(String, unique=True, nullable=False)