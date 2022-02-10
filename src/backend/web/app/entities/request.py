from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Request(SQLModel, table=True):
    id: int = Field(primary_key=True)
    hash: Optional[str] = None
    stmt: str
    