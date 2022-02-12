import requests
import tensorflow as tf
import tensorflow_datasets as tfds

candidates = [
    "oxford_flowers102",
    "mnist",
    "caltech101",
    "cifar10",
    "cifar100",
    "patch_camelyon",
]

for each in candidates:
    builder = tfds.builder(each)
    info = builder.info
    num_classes = info.features["label"].num_classes
    for split in info.splits.keys():
        size = info.splits[split].num_examples
        name = "tfds/{}/{}".format(info.name, split)
        json = {
            "tfds_name": info.name,
            "split": split,
            "feature": "image",
            "label": "label",
        }
        res = requests.post(
            "http://localhost:8081/datasets",
            json={
                "name": name,
                "json_dataset": str(json),
                "size": size,
                "num_classes": num_classes,
            },
        )
        print(res.text)
