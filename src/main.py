from fastapi import FastAPI
from src.database.database import engine, Base
from src.crud import orden_crud
from src.schemas.orden_schema import OrdenCreate
from src.database.database import SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def inicio():
    return {"mensaje": "API Ecommerce funcionando"}