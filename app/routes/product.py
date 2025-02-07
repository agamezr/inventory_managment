from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.crud.product import get_all_products
from app.crud.product import get_product_by_id
from app.crud.product import create_product
from app.schemas.product import ProductSchema, ProductNew, ProductShow
from app.config.dependencies import get_db
from typing import List, Optional

product = APIRouter()

@product.get("/products", response_model=List[ProductSchema])
def get_products(
        db: Session = Depends(get_db),
        page: int = Query(ge=1, default=1, required=False),
        per_page: int = Query(ge=1, le=100, default=10, required=False),
        category: Optional[str] = Query(None, description="Category"),
        min_price: Optional[float] = Query(None, description="Min Price"),
        max_price: Optional[float] = Query(None, description="Max Price"),
        stock: Optional[int] = Query(None, description="Min Stock")
    ):
    return get_all_products(db, page, per_page, category, min_price, max_price, stock)

@product.get("/products/{id}", response_model=ProductSchema)
def get_product_detail(id: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product.post("/products", response_model=ProductShow)
def new_product(product_params: ProductNew, db: Session = Depends(get_db)):
    try:
        product = create_product(db, product_params)
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
