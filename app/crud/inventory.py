from sqlalchemy.orm import Session, joinedload
from app.models.inventory import Inventory

def get_inventory_by_store(db: Session, store_id: str):
    return db.query(Inventory).options(joinedload(Inventory.product)).filter(Inventory.store_id == store_id).all()