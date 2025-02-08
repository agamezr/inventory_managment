from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.inventory import InventorySchema
from app.config.dependencies import get_db
from app.crud.inventory import get_inventory_by_store
from typing import List

inventory = APIRouter()

@inventory.get("/stores/{id}/inventory", response_model=List[InventorySchema])
def inventory_by_store(id: str, db :Session = Depends(get_db)):
    inventory_data = get_inventory_by_store(db, id)
    if not inventory_data:
        raise HTTPException(status_code=404, detail="No inventory found.")
    
    return inventory_data




