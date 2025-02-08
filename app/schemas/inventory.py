from pydantic import BaseModel, PositiveInt
from typing import Optional
from app.schemas.product import ProductShowSchema

class BaseInventorySchema(BaseModel):
    id: str
    product_id: str
    store_id: str
    quantity: int
    min_stock: int
    product: Optional[ProductShowSchema]

    class Config:
        from_attributes = True

class InventorySchema(BaseInventorySchema):
    pass

class InventoryTransferSchema(BaseModel):
    product_id: str
    origin_store_id: str
    target_store_id: str
    quantity: PositiveInt

    class Config:
        from_attributes = True

class InventoryLowStockSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    sku: str
    store_id: str
    quantity: int
    min_stock: int

    class Config:
        from_attributes = True