from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from config.db import conn
# from models.task import tasks
# from schemas.task import Task

inventory = APIRouter()

@inventory.get("/inventories")
def index():
    return { "inventorys": "hola app" }