from sqlalchemy.orm import Session
from app.models.product import Product

def get_all_products(
        db: Session,
        page: int = 0,
        per_page: int = 10,
        category: str = None, 
        min_price: float = None, 
        max_price: float = None, 
        ):
    products = db.query(Product)

    if category:
        products = products.filter(Product.category == category)
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)

    return products.limit(per_page).offset(
                    page - 1
                    if page == 1
                    else (page - 1) * per_page
                ).all()