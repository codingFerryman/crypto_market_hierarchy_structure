import json

import pandas as pd
import requests

"""
class SealModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    json_model: str
    num_params: Optional[int] = None
    feat_size: int
    input_spec: str
    owner: str = Field(default='public')
"""

image_models = pd.read_csv("scripts/image_models.csv")
for idx, row in image_models.iterrows():
    json_model = str(json.loads(row["json_model"]))
    num_params = row["num_params"]
    feat_size = row["dimension"]
    up_acc = float(row["up_acc"])
    input_spec = str(
        {
            "image_size": row["image_size"],
        }
    )

    res = requests.post(
        "http://localhost:8080/models",
        json={
            "json_model": json_model,
            "feat_size": feat_size,
            "input_spec": input_spec,
            "num_params": num_params,
            "up_acc": up_acc,
        },
    )

    print(res.text)
