from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.product import get_all_products
from app.schemas.product import ProductSchema
from app.config.dependencies import get_db
from typing import List

product = APIRouter()

@product.get("/products", response_model=List[ProductSchema])
def read_products(db: Session = Depends(get_db)):
    return get_all_products(db)

