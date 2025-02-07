from pydantic import BaseModel
from typing import Optional

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
