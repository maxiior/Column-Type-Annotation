from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import numpy as np
import re
import pathlib
import time
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

TABLES_FOLDER_DIR = str(pathlib.Path(
    __file__).parent.resolve()) + '\\tables'

TARGETS_FILE_NAME = str(pathlib.Path(
    __file__).parent.resolve()) + '\\definitive_files.csv'

column_items = []

def preporcess_item(word):
    word = re.sub(' \*? ?(A|a)lso.*', '', word)
    word = re.sub('(\(|\[).*(\)|\])', '', word)
    word = re.sub('[^A-Za-z0-9 \-\d+/\d+\?]+', '', word)
    word = re.sub('( |\-){1,}', '_', word)
    word = word.replace("__", "_")
    word = re.sub('(^_|_$)', '', word)
    return word

# Wyjmujemy poszczególne kolumny z określonych tabel i umieszczamy jes w column_items


def get_column_items(row):
    global column_items
    name = row["name"]
    position = row["position"]

    df = pd.read_csv(TABLES_FOLDER_DIR + "\\" + name + ".csv")

    cells = []
    column = df.iloc[:, position]

    for _, value in column.items():
        value = preporcess_item(str(value))
        if not (pd.isna(value)):
            cells.append(value)
    items = dict()
    items['name'] = name
    items['position'] = position
    items['items'] = cells
    column_items.append(items)

# Pobieramy klasy określające daną komórkę


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
    time.sleep(0.3)

    return respond


def get_size(column_items):
    q = 0
    for column in column_items:
        for _ in column['items']:
            q += 1
    print('size: ', q, '(~', str(round(q*0.8/60)), 'min)')


def get_items_classes():
    df_targets = pd.read_csv(TARGETS_FILE_NAME)

    for i in df_targets.iloc:
        get_column_items(i)

    print("Wyjmowanie komórek z kolumn: DONE")

    items_classes = []

    get_size(column_items)

    q = 0
    for column in column_items:
        item_classes = dict()
        item_classes['name'] = column['name']
        item_classes['position'] = column['position']
        item_classes['class'] = []

        q += 1
        if q % 40 == 0:
            time.sleep(30)
        print(q, '/', len(column_items))

        for item in column['items']:
            tmp = get_ontology_classes(item)[0]
            for i in tmp:
                item_classes['class'].append(i)
        try:
            item_classes['class'] = max(
                set(item_classes['class']), key=item_classes['class'].count)
        except:
            item_classes['class'] = None
        items_classes.append(item_classes)

    tmp = []
    for i in items_classes:
        if i['class'] != None:
            tmp.append(i)

    items_classes = tmp

    print("Pobieranie klas dla komórek: DONE")

    #Tworzymy DataFrame, w którym dla każdego itemu przypiszemy pobrane klasy
    items_classes_df = pd.DataFrame.from_dict(items_classes)
    items_classes_df.to_csv('items_classes.csv', index=False)
