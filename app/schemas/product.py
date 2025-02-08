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

class ProductNewSchema(BaseModel):
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
    
class ProductShowSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    sku: str

    class Config:
        orm_mode = True


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100, example="Updated Product")
    description: Optional[str] = Field(None, max_length=255, example="Updated description")
    category: Optional[str] = Field(None, min_length=3, max_length=50, example="Updated Electronics")
    price: Optional[float] = Field(None, gt=0, example=899.99) 
    sku: Optional[str] = Field(None, min_length=5, max_length=20, example="NEW-SKU")

    @validator("sku")
    def validate_sku(cls, value):
        if value and not re.match(r"^[A-Za-z0-9_-]+$", value):
            raise ValueError("SKU must be alphanumeric.")
        return value