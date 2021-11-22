from re import sub
import pandas as pd

def get_efficiency():
    submission = pd.read_csv('model_submission.csv')

    q=0
    for i in submission.iloc:
        q+=1
    print(q)

    answear = pd.DataFrame()

    correct = 0

    for i in submission.iloc:
        answear = pd.read_csv("tables\\" + i[0] + ".csv")

        if answear.columns[i[1]].lower() == i[2].replace('http://dbpedia.org/ontology/','').lower():
            correct += 1

    print(correct)