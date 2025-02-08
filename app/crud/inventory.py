from sqlalchemy.orm import Session, joinedload
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryTransfer
from sqlalchemy.exc import IntegrityError
import uuid
from fastapi import HTTPException

def get_inventory_by_store(db: Session, store_id: str):
    return db.query(Inventory).options(joinedload(Inventory.product)).filter(Inventory.store_id == store_id).all()

def transfer_inventory_products(db: Session, transfer_params: InventoryTransfer):
    origin_inventory_data = db.query(Inventory).filter(
            Inventory.store_id == transfer_params.origin_store_id,
            Inventory.product_id == transfer_params.product_id
        ).first()

    if not origin_inventory_data:
        raise HTTPException(status_code=404, detail="Product not found in origin store!")

    if origin_inventory_data.quantity < transfer_params.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock in origin store!")

    if (origin_inventory_data.quantity - transfer_params.quantity) < origin_inventory_data.min_stock:
        raise HTTPException(status_code=400, detail="Not enough min stock in origin store!")

    target_inventory_data = db.query(Inventory).filter(
            Inventory.store_id == transfer_params.target_store_id,
            Inventory.product_id == transfer_params.product_id
        ).first()
    
    if not target_inventory_data:
        target_inventory_data = Inventory(
            id = str(uuid.uuid4()),
            product_id = transfer_params.product_id,
            store_id = transfer_params.target_store_id,
            quantity = 0,
            min_stock = 5,
        )
        db.add(target_inventory_data)
        db.flush()

    origin_inventory_data.quantity -= transfer_params.quantity
    target_inventory_data.quantity += transfer_params.quantity

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during transfer")

    return {"message": "Transfer successful"}
