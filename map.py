import pandas as pd

REPLACE = [".", ":", "'", "-", "/", "?", "*", ",", "&",
           "(", ")", "!", "[", "]", "=", ">", "+", ";", '"']


def process_data(text):
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
        lambda x: " ; ".join(process_data(x)))
    data.to_csv("dataset_dbpedied.csv", index=False)