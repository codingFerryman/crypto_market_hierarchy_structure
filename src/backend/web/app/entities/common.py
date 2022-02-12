from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class SealModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    json_model: str
    num_params: Optional[int] = None
    feat_size: int
    input_spec: str
    up_acc: Optional[float]
    owner: str = Field(default="public")


class SealDataset(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    json_dataset: str
    size: int
    num_classes: int
    owner: str = Field(default="public")


class Request(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    hash: Optional[str] = None
    stmt: str
