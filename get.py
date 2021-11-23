import pandas as pd


def get_files_of_size(MAX_FILE_SIZE=1000000):
    files = pd.read_csv("CTA_DBP_Round1_Targets.csv")
    definitive_files = pd.DataFrame(columns=['name', 'position'])

    table = pd.DataFrame()

    for i in files.iloc:
        table = pd.read_csv('tables\\' + i[0] + ".csv")

        # Sprawdzamy, czy table ma mniej niż MAX_FILE_SIZE wierszy
        if table[table.columns.tolist()[0]].size < MAX_FILE_SIZE:
            definitive_files = definitive_files.append(
                {'name': i.iloc[0], 'position': i.iloc[1]}, ignore_index=True)

    definitive_files.to_csv("definitive_files.csv", index=False)


def get_classes_for_files_columns():
    items_classes = pd.read_csv("items_classes.csv")

    classes_that_work = [i['class'].lower() for i in items_classes.iloc]

    print('Liczba wierszy definitive_files.csv: ',
          items_classes['name'].size)

    df = pd.DataFrame()

    for i in items_classes.iloc:
        csv = pd.read_csv("tables\\" + i['name'] + ".csv")
        s = ""

        column = csv[csv.columns.tolist()[int(i['position'])]]
        for k, j in enumerate(column):
            if k == len(column) - 1:
                s += "\"" + str(j) + "\""
            else:
                s += "\"" + str(j) + "\";"

        row = {'csv': i['name'], 'position': str(
            int(i['position'])), 'text': s}

        for j in classes_that_work:
            if i['class'].lower() == j.lower():
                row[j] = str(int(1))
            else:
                row[j] = str(int(0))

        df = df.append(row, ignore_index=True)
    df.to_csv("dataset.csv", index=False)
