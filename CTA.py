from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import numpy as np
import os
import re
import pathlib
import time

target_dir = './dataset/Round1/targets'
gt_dir = './dataset/Round1/gt'
TABLES_FOLDER_DIR = str(pathlib.Path(
    __file__).parent.resolve()) + '\\tables'

TARGETS_FILE_NAME = str(pathlib.Path(
    __file__).parent.resolve()) + '\\CTA_DBP_Round1_Targets.csv'

df_targets = pd.read_csv(TARGETS_FILE_NAME,
                         header=None,
                         nrows=540,
                         names=['table_id', 'column_id'],
                         dtype={'column_id': np.int8})


def preporcess_item(word):
    word = re.sub(' \*? ?(A|a)lso.*', '', word)
    word = re.sub('(\(|\[).*(\)|\])', '', word)
    word = re.sub('[^A-Za-z0-9 \-\d+/\d+\?]+', '', word)
    word = re.sub('( |\-){1,}', '_', word)
    word = word.replace("__", "_")
    word = re.sub('(^_|_$)', '', word)
    return word


column_items = []


def get_column_items(row):
    global column_items
    table_id = row["table_id"]
    column_id = row["column_id"]

    print(TABLES_FOLDER_DIR + "\\" + table_id + ".csv")
    df = pd.read_csv(TABLES_FOLDER_DIR + "\\" + table_id + ".csv")
    cells = []
    column = df.iloc[:, column_id]

    for _, value in column.items():
        value = preporcess_item(str(value))
        if not (pd.isna(value)):
            cells.append(value)
    column_items.append(cells)


for i in df_targets.iloc:
    get_column_items(i)


def get_ontology_classes(item):
    respond = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?type
        WHERE { <http://dbpedia.org/resource/"""+item+"""> rdf:type ?type }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    respond.append([result["type"]["value"] for result in results["results"]["bindings"]
                    if 'http://dbpedia.org/ontology' in result["type"]["value"]])

    return respond


items_classes = []

for column in column_items:
    item_classes = []
    for item in column:
        item_classes.append(get_ontology_classes(item))
    items_classes.append(item_classes)

items_classes_df = pd.DataFrame(columns=['item', 'classes'])

for items in items_classes:
    res = [items[i] for i in (0, -1)]
    items_classes_df = items_classes_df.append({'item': res[0], 'classes': ";".join(
        map((lambda x: '"' + str(x) + '"'), res[1]))}, ignore_index=True)

mask = (items_classes_df['classes'] == '')
items_classes_df['classes'][mask] = '"' + items_classes_df['item'] + '"'

items_classes_df.to_csv('items_classes_df_p.csv', index=False)
