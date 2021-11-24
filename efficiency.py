from re import sub
import pandas as pd


def get_efficiency(show):
    submission = pd.read_csv('model_submission.csv')

    all = 0
    for i in submission.iloc:
        all += 1

    answear = pd.DataFrame()

    correct = 0

    for i in submission.iloc:
        answear = pd.read_csv("tables\\" + i[0] + ".csv")

        a = [answear.columns[i[1]].lower(), i[2].replace(
            'http://dbpedia.org/ontology/', '').lower()]

        if a[0] == a[1]:
            if show:
                print(i[0], i[1], a, "TRUE")
            correct += 1
        else:
            if show:
                print(i[0], i[1], a, "FALSE")

    print(correct, "/", all, round(correct/all, 2))
