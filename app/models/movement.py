from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, Enum
from datetime import datetime
from app.config.database import meta, engine, Base
import enum


class MovementType(enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"

class Movement(Base):
    __tablename__ = 'movements'

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'), nullable=False)
    source_store_id = Column(String, nullable=True)
    target_store_id = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    type = Column(Enum(MovementType), nullable=False)