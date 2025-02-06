from fastapi import FastAPI
from app.routes.inventory import inventory

app = FastAPI()

app.include_router(inventory)