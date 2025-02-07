from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.inventory import Inventory
from sqlalchemy.sql import func

def get_all_products(
        db: Session,
        page: int = 0,
        per_page: int = 10,
        category: str = None, 
        min_price: float = None, 
        max_price: float = None,
        stock: int = None
        ):

    products =  db.query(
        Product.id,
        Product.name,
        Product.description,
        Product.category,
        Product.price,
        Product.sku,
        func.coalesce(func.sum(Inventory.quantity), 0).label("available_stock")
    ).outerjoin(Inventory).group_by(Product.id)

    if category:
        products = products.filter(Product.category == category)
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
    if stock is not None:
        products = products.having(func.coalesce(func.sum(Inventory.quantity), 0) >= stock)


    return products.limit(per_page).offset(
                    page - 1
                    if page == 1
                    else (page - 1) * per_page
                ).all()

def get_product_by_id(db: Session, id: str):
    return db.query(
        Product.id,
        Product.name,
        Product.description,
        Product.category,
        Product.price,
        Product.sku,
        func.coalesce(func.sum(Inventory.quantity), 0).label("available_stock")
    ).outerjoin(Inventory).filter(Product.id == id).group_by(Product.id).first()

