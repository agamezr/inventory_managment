from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.crud.product import get_all_products
from app.schemas.product import ProductSchema
from app.config.dependencies import get_db
from typing import List

product = APIRouter()

@product.get("/products", response_model=List[ProductSchema])
def read_products(
        db: Session = Depends(get_db),
        page: int = Query(ge=1, default=1, required=False),
        per_page: int = Query(ge=1, le=100, default=10, required=False)
    ):
    return get_all_products(db, page, per_page)
