from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.crud.product import get_all_products
from app.schemas.product import ProductSchema
from app.config.dependencies import get_db
from typing import List, Optional

product = APIRouter()

@product.get("/products", response_model=List[ProductSchema])
def read_products(
        db: Session = Depends(get_db),
        page: int = Query(ge=1, default=1, required=False),
        per_page: int = Query(ge=1, le=100, default=10, required=False),
        category: Optional[str] = Query(None, description="Categoría del producto"),
        min_price: Optional[float] = Query(None, description="Precio mínimo"),
        max_price: Optional[float] = Query(None, description="Precio máximo")
    ):
    return get_all_products(db, page, per_page, category, min_price, max_price)

