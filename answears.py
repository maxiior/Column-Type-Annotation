import pandas as pd

def get_correct_answears():
    df = pd.read_csv("CTA_DBP_Round1_Targets.csv")
    answears = []

    for i in df.iloc:
        csv = pd.read_csv("tables\\" + i[0] + ".csv")
        answears.append('http://dbpedia.org/ontology/' +
                        csv.columns.tolist()[i[1]])

    df['answears'] = answears
    df.to_csv("answears.csv", index=False, header=False)
    f = open('answears.csv', 'r')
    lines = []

    for i in f:
        tab = str(i).split(',')
        s = '\"' + tab[0] + '\",'
        s += '\"' + tab[1] + '\",'
        s += '\"' + tab[2].replace('\n', '') + '\"\n'
        lines.append(s)
    f.close()

    f = open('answears.csv', 'a')
    f.truncate(0)

    for i in lines:
        f.write(i)
    f.close()