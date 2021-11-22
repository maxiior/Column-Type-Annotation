import pandas as pd

MAX_FILE_SIZE = 100

def get_classes_for_files_columns():
    file_names = pd.read_csv("CTA_DBP_Round1_Targets.csv")
    classes_that_work = []

    f = open("classes_that_work.txt", "r")
    for i in f:
        classes_that_work.append(i.replace('\n', '').lower())
    f.close()

    definitive_files = pd.DataFrame(columns=['name', 'position'])
    df = pd.DataFrame()

    for i in file_names.iloc:
        df = pd.read_csv('tables\\' + i[0] + ".csv")

        if df[df.columns.tolist()[0]].size < MAX_FILE_SIZE:
            for j in df.columns:
                if df.columns.tolist().index(j) == i[1] and j.lower() in classes_that_work:
                    definitive_files = definitive_files.append(
                        {'name': i.iloc[0], 'position': i.iloc[1]}, ignore_index=True)

    definitive_files.to_csv("definitive_files.csv", index=False, header=False)

    columns = ['csv', 'text']
    for i in classes_that_work:
        columns.append('http://dbpedia.org/ontology/' + i)

    print('Definitive columns: ', definitive_files['name'].size)

    df = pd.DataFrame(columns=columns)

    for i in definitive_files.iloc:
        csv = pd.read_csv("tables\\" + i[0] + ".csv")
        s = ""

        for k, j in enumerate(csv[csv.columns.tolist()[i[1]]]):
            if k == len(csv[csv.columns.tolist()[i[1]]]) - 1:
                s += "\"" + str(j) + "\""
            else:
                s += "\"" + str(j) + "\";"

        classe = {'csv': i[0], 'text': s}

        for j in classes_that_work:
            if j in [i.lower() for i in csv.columns.tolist()]:
                if i[1] == [i.lower() for i in csv.columns.tolist()].index(j):
                    classe['http://dbpedia.org/ontology/'+j] = 1
                else:
                    classe['http://dbpedia.org/ontology/'+j] = 0
            else:
                classe['http://dbpedia.org/ontology/'+j] = 0

        df = df.append(classe, ignore_index=True)

    df.to_csv("dataset.csv", index=False)