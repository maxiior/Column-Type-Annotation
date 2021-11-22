from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import numpy as np
import re
import pathlib
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

column_items = []

TABLES_FOLDER_DIR = str(pathlib.Path(
    __file__).parent.resolve()) + '\\tables'

TARGETS_FILE_NAME = str(pathlib.Path(
    __file__).parent.resolve()) + '\\definitive_files.csv'

def preporcess(word):
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
        value = preporcess(str(value))
        if not (pd.isna(value)):
            cells.append(value)
    column_items.append(cells)

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
    time.sleep(0.32)

    return respond


def get_size(column_items):
    q = 0
    for column in column_items:
        for _ in column:
            q += 1
    print('size: ', q, '(~', str(round(q*0.8/60)), 'min)')


def get_items_classes():
    df_targets = pd.read_csv(TARGETS_FILE_NAME,
                        header=None,
                        names=['name', 'position'],
                        dtype={'position': np.int8})

    for i in df_targets.iloc:
        get_column_items(i)
    get_size(column_items)
    print("Wyjmowanie komórek z kolumn: DONE\n")

    items_classes = []
    q = 0
    for column in column_items:
        item_classes = []
        q += 1
        if q % 15 == 0:
            time.sleep(30)
        print(q, '/', len(column_items))
        for item in column:
            item_classes.append(get_ontology_classes(item))
        items_classes.append(item_classes)

    print("Pobieranie klas dla poszczególnych komórek kolumn: DONE\n")

    # Tworzymy DataFrame, w którym dla każdego itemu przypiszemy pobrane klasy
    items_classes_df = pd.DataFrame(columns=['item', 'classes'])

    for items in items_classes:
        res = [items[i] for i in (0, -1)]
        items_classes_df = items_classes_df.append({'item': res[0], 'classes': ";".join(
            map((lambda x: '"' + str(x) + '"'), res[1]))}, ignore_index=True)

    mask = (items_classes_df['classes'] == '')
    items_classes_df['classes'][mask] = '"' + \
        str(items_classes_df['item']) + '"'

    items_classes_df.to_csv('items_classes.csv', index=False)