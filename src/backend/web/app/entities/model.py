from typing import Optional
from sqlmodel import Field, SQLModel

class SealModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    json_model: str
    num_params: Optional[int] = None
    feat_size: int
    input_spec: str
    owner: str = Field(default='public')

