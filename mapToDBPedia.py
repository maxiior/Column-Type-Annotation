import pandas as pd

df = pd.read_csv("items_classes_df.csv")

df = df.fillna("")

classes_translated = {}
for cc, row in df.iterrows():
    classes_translated[row["item"]] = row["classes"]


dane = pd.read_csv("glove_df_p.csv")

dane = dane.fillna("")

def process_data(text, classes_translated):
    splt = text.split('";"')
    toret = []
    for item in splt:
        item = item.replace('"', "")\
            .replace(" ","_")\
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
            newitem = newitem.replace("http://dbpedia.org/ontology/", "").replace("_", " ")
        toret.append(newitem)
        
    return toret

dane["text_dbpedied"] = dane["text"].apply(lambda x: " ; ".join(process_data(x, classes_translated)))

dane.to_csv("glove_df_dbpedied_p.csv")