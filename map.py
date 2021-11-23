import pandas as pd

REPLACE = [".", ":", "'", "-", "/", "?", "*", ",", "&",
           "(", ")", "!", "[", "]", "=", ">", "+", ";", '"']


def preprocess(text):
    splt = text.split('";"')
    toret = []
    for item in splt:
        for i in REPLACE:
            item = item.replace(i, "")
        item = item.replace(" ", "_")\
            .replace("__", "_")
        item = item.replace('";"', '" ; "').replace("_", " ")
        toret.append(item)
    return toret


def map_items():
    data = pd.read_csv("dataset.csv")
    data = data.fillna("")
    data["text_dbpedied"] = data["text"].apply(
        lambda x: " ; ".join(preprocess(x)))
    data = data.drop_duplicates(subset=["text"])
    data = data.drop(["text"], axis=1)
    data.to_csv("dataset_dbpedied.csv", index=False)
    print("Mapowanie: DONE")
