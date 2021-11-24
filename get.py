import pandas as pd

def get_classes_that_work():
    classes_that_work = []
    f = open("classes_that_work.txt", "r")
    for i in f:
        classes_that_work.append(i.replace('\n', '').lower())
    f.close()
    return classes_that_work


def get_files_of_size(MAX_FILE_SIZE=1000000):
    files = pd.read_csv("CTA_DBP_Round1_Targets.csv")

    classes_that_work = get_classes_that_work()

    definitive_files = pd.DataFrame(columns=['name', 'position'])
    table = pd.DataFrame()

    for i in files.iloc:
        table = pd.read_csv('tables\\' + i[0] + ".csv")

        # Sprawdzamy, czy table ma mniej niż MAX_FILE_SIZE wierszy
        if table[table.columns.tolist()[0]].size < MAX_FILE_SIZE:
            for j in table.columns:
                if table.columns.tolist().index(j) == i[1] and j.lower() in classes_that_work:
                    definitive_files = definitive_files.append(
                        {'name': i.iloc[0], 'position': i.iloc[1]}, ignore_index=True)

    definitive_files.to_csv("definitive_files.csv", index=False)
    print(f'get_files_of_size | Wybieranie plików o {MAX_FILE_SIZE} wierszach: DONE')
    print(f'get_files_of_size | Utworzenie pliku definitive_files.csv: DONE')


def get_classes_for_files_columns(MAX_FILE_SIZE=1000000):
    definitive_files = pd.read_csv("definitive_files.csv")
    classes_that_work = get_classes_that_work()

    print('get_classes_for_files_columns | Liczba wierszy definitive_files.csv: ',
          definitive_files['name'].size)

    df = pd.DataFrame()

    for i in definitive_files.iloc:
        csv = pd.read_csv("tables\\" + i['name'] + ".csv")
        s = ""

        for k, j in enumerate(csv[csv.columns.tolist()[i['position']]]):
            if k == len(csv[csv.columns.tolist()[i['position']]]) - 1:
                s += "\"" + str(j) + "\""
            else:
                s += "\"" + str(j) + "\";"

        classe = {'csv': i['name'], 'position': str(int(i['position'])), 'text': s}

        for j in classes_that_work:
            # jeżeli klasa j znajduje się na liście kolumn pliku i...
            if j in [i.lower() for i in csv.columns.tolist()]:
                # jeżeli indeks pliku i równy jest indeksowi klasy j w tym pliku...
                if i['position'] == [i.lower() for i in csv.columns.tolist()].index(j):
                    classe['http://dbpedia.org/ontology/'+j] = 1
                else:
                    classe['http://dbpedia.org/ontology/'+j] = 0
            else:
                classe['http://dbpedia.org/ontology/'+j] = 0

        df = df.append(classe, ignore_index=True)
    df.to_csv("dataset.csv", index=False)

    print('get_classes_for_files_columns | Przypisanie elementów kolumn: DONE')
    print('get_classes_for_files_columns | Utworzenie pliku dataset.csv: DONE')
