from typing import Optional
from fastapi import FastAPI
import boto3

app = FastAPI()
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://dynamodb-local:8000",
    region_name='eu-central-1',
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
