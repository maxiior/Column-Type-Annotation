from re import sub
import pandas as pd


def get_efficiency(show):
    submission = pd.read_csv('model_submission.csv', header=None)
    answears = pd.read_csv('items_classes.csv')

    all = 0
    for i in submission.iloc:
        all += 1

    correct = 0

    for i in submission.iloc:
        for j in answears.iloc:
            if i[0] == j['name'] and i[1] == j['position']:
                prediction = i[2].lower()
                answear = j['class'].lower()
                if prediction == answear:
                    if show:
                        print(i[0], prediction, answear, "TRUE")
                    correct+=1
                else:
                    if show:
                        print(i[0], prediction, answear, "FALSE")

    print(correct, "/", all, round(correct/all, 2))