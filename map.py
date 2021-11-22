import pandas as pd

def process_data(text, classes_translated):
    splt = text.split('";"')
    toret = []
    for item in splt:
        item = item.replace('"', "")\
            .replace(" ", "_")\
            .replace(".", "")\
            .replace(":", "")\
            .replace("'", "")\
            .replace("-", "")\
            .replace("/", "")\
            .replace("?", "")\
            .replace("*", "")\
            .replace(",", "")\
            .replace("&", "")\
            .replace("(", "")\
            .replace(")", "")\
            .replace("!", "")\
            .replace("[", "")\
            .replace("]", "")\
            .replace("=", "")\
            .replace(">", "")\
            .replace("+", "")\
            .replace(";", "")\
            .replace('"', "")\
            .replace("__", "_")
        if item == "nan":
            newitem = item.replace('";"', '" ; "').replace("_", " ")
        if item not in classes_translated.keys():
            newitem = item.replace('";"', '" ; "').replace("_", " ")
        else:
            newitem = classes_translated[item].replace('";"', '" ; "')
            newitem = newitem.replace(
                "http://dbpedia.org/ontology/", "").replace("_", " ")
        toret.append(newitem)
    return toret

def map_items():
    df = pd.read_csv("items_classes.csv")
    df = df.fillna("")

    classes_translated = {}
    for _, row in df.iterrows():
        classes_translated[row["item"]] = row["classes"]

    data = pd.read_csv("dataset.csv")
    data = data.fillna("")

    data["text_dbpedied"] = data["text"].apply(
        lambda x: " ; ".join(process_data(x, classes_translated)))
    data.to_csv("dataset_dbpedied.csv")