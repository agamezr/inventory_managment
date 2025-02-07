from sqlalchemy.orm import Session
from app.models.product import Product

def get_all_products(db: Session, page: int = 0, per_page: int = 10):
    return db.query(
                Product).limit(per_page).offset(
                    page - 1
                    if page == 1
                    else (page - 1) * per_page
                ).all()