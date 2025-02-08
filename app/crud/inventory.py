from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.inventory import Inventory
from app.models.movement import Movement, MovementType
from app.models.product import Product
from app.schemas.inventory import InventoryTransferSchema
from sqlalchemy.exc import IntegrityError
import uuid
from datetime import datetime

def get_inventory_by_store(db: Session, store_id: str):
    return db.query(Inventory).options(joinedload(Inventory.product)).filter(Inventory.store_id == store_id).all()

def transfer_inventory_products(db: Session, transfer_params: InventoryTransferSchema):
    try:
        with db.begin():
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

            movement = Movement(
                id = str(uuid.uuid4()),
                product_id = transfer_params.product_id,
                source_store_id = transfer_params.origin_store_id,
                target_store_id = transfer_params.target_store_id,
                quantity = transfer_params.quantity,
                timestamp = datetime.utcnow(),
                type = MovementType.TRANSFER
            )
            db.add(movement)

        return {"message": "Transfer successful!"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during transfer!")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def get_low_stock_products(db: Session):
    return db.query(
        Product.id,
        Product.name,
        Product.description,
        Product.category,
        Product.price,
        Product.sku,
        Inventory.store_id,
        Inventory.quantity,
        Inventory.min_stock
    ).join(Inventory, Inventory.product_id == Product.id).filter(Inventory.quantity < Inventory.min_stock).all()


