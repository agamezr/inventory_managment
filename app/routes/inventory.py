from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.inventory import InventorySchema
from app.schemas.inventory import InventoryTransfer, InventoryLowStock
from app.config.dependencies import get_db
from app.crud.inventory import get_inventory_by_store, transfer_inventory_products, get_low_stock_products
from typing import List

inventory = APIRouter()

@inventory.get("/stores/{id}/inventory", response_model=List[InventorySchema])
def inventory_by_store(id: str, db: Session = Depends(get_db)):
    inventory_data = get_inventory_by_store(db, id)
    if not inventory_data:
        raise HTTPException(status_code=404, detail="No inventory found.")

    return inventory_data

@inventory.post("/inventory/transfer")
def transfer_products(transfer_params: InventoryTransfer, db: Session = Depends(get_db)):
    return transfer_inventory_products(db, transfer_params)

@inventory.get("/inventory/alerts", response_model = List[InventoryLowStock])
def inventory_low(db: Session = Depends(get_db)):
    return get_low_stock_products(db)