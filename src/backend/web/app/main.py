from functools import lru_cache
from typing import List

from app.entities.common import Request, SealDataset, SealModel
from app.modules.config import settings
from fastapi import FastAPI, status
from sqlmodel import Session, SQLModel, create_engine, select

app = FastAPI()


@lru_cache
def get_settings():
    return settings.Settings()


@lru_cache
def get_engine():
    settings = get_settings()
    pg_url = "postgresql://{}@{}:{}".format(
        settings.pg_user, settings.pg_host, settings.pg_port
    )
    engine = create_engine(pg_url)
    return engine


session = Session(bind=get_engine())


@app.get("/create")
async def create():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


@app.get("/datasets", response_model=List[SealDataset], status_code=status.HTTP_200_OK)
async def get_all_datasets():
    engine = get_engine()
    statement = select(SealDataset)
    with Session(engine) as session:
        datasets = session.exec(statement).all()
        return datasets


@app.post("/datasets", response_model=SealDataset, status_code=status.HTTP_201_CREATED)
async def create_a_dataset(dataset: SealDataset):
    engine = get_engine()
    session.add(dataset)
    session.commit()
    return dataset


@app.get("/models", response_model=List[SealModel], status_code=status.HTTP_200_OK)
async def get_all_models():
    engine = get_engine()
    statement = select(SealModel)
    with Session(engine) as session:
        models = session.exec(statement).all()
        return models


@app.post("/models", response_model=SealModel, status_code=status.HTTP_201_CREATED)
async def create_a_model(model: SealModel):
    engine = get_engine()
    session.add(model)
    session.commit()
    return model
