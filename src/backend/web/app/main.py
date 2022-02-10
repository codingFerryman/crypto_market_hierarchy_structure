import os
from typing import Optional
from fastapi import FastAPI
from app.entities.model import SealModel

from sqlmodel import create_engine, SQLModel

PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']
PG_USER = os.environ['PG_USER']

app = FastAPI()
pg_url = "postgresql://{}@{}:{}".format(PG_USER, PG_HOST, PG_PORT)
engine = create_engine(pg_url)
SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
