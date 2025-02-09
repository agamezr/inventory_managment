from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.inventory import Inventory
from sqlalchemy.sql import func
from app.schemas.product import ProductNewSchema
from sqlalchemy.exc import IntegrityError
import uuid

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

def create_product(db: Session, product_params: ProductNewSchema):
    try:
        with db.begin():
            existing_product = db.query(Product).filter(Product.sku == product_params.sku).first()
            if existing_product:
                raise ValueError("SKU already exists!")
            
            product = Product(
                id = str(uuid.uuid4()),
                name = product_params.name,
                description = product_params.description,
                category = product_params.category,
                price = product_params.price,
                sku = product_params.sku
            )
            db.add(product)
        
        db.refresh(product)
        return product

    except IntegrityError:
        db.rollback()
        raise ValueError("Databse error: Unable to create product!")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def update_product(db: Session, id: str, product_params: ProductNewSchema):
    try:
        with db.begin():
            product = db.query(Product).filter(Product.id == id).first()

            print(product)
            if not product:
                return None

            if product_params.sku:
                existing_product = db.query(Product).filter(Product.sku == product_params.sku).first()
                if existing_product and existing_product.id != product.id:
                    raise ValueError("SKU already exists!")
            
            for field, value in product_params.dict(exclude_unset=True).items():
                setattr(product, field, value)

        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise ValueError("Database error: Unable to update product!")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_product(db: Session, product_id: str):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return None

    try:
        db.delete(product)
        db.commit()
        return product
    except IntegrityError:
        db.rollback()
        raise ValueError("Database error: Unable to delete product!")