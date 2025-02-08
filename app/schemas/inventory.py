from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductShow

class InventorySchema(BaseModel):
    id: str
    product_id: str
    store_id: str
    quantity: int
    min_stock: int
    product: Optional[ProductShow]

    class Config:
        orm_mode = True