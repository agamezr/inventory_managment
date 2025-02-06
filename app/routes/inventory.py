from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

inventory = APIRouter()

@inventory.get("/inventories")
def index():
    return { "inventorys": "hola app" }