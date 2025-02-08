from pydantic import BaseModel, PositiveInt
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

class InventoryTransfer(BaseModel):
    product_id: str
    origin_store_id: str
    target_store_id: str
    quantity: PositiveInt

    class Config:
        orm_mode = True