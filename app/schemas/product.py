from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ProductSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    sku: str
    available_stock: int

    class Config:
        orm_mode = True

class ProductNew(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Laptop")
    description: Optional[str] = Field(None, max_length=255, example="Asus Laptop 32GB RAM")
    category: str = Field(..., min_length=3, max_length=50, example="Electronics")
    price: float = Field(..., gt=0, example=999.99)
    sku: str = Field(..., min_length=5, max_length=20, example="LAPASUS123")

    @validator("sku")
    def validate_sku(cls, value):
        if not re.match(r"^[A-Za-z0-9_-]+$", value):
            raise ValueError("SKU must be alphanumeric.")
        return value
    
class ProductShow(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    sku: str

    class Config:
        orm_mode = True