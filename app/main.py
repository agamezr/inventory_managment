from fastapi import FastAPI
from app.routes.inventory import inventory
from app.routes.product import product

app = FastAPI()

app.include_router(inventory)
app.include_router(product)