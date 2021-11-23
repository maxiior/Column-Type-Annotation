import pandas as pd


def get_correct_answears():
    df = pd.read_csv("definitive_files.csv")
    answears = []

    for i in df.iloc:
        csv = pd.read_csv("tables\\" + i[0] + ".csv")
        answears.append('http://dbpedia.org/ontology/' +
                        csv.columns.tolist()[i[1]])

    df['answears'] = answears
    df.to_csv("answears.csv", index=False, header=False)
