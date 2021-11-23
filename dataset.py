import pandas as pd
import numpy as np
from collections import Counter


def create_train_test_dataset():
    df = pd.read_csv("dataset_dbpedied.csv")
    df = df.drop_duplicates(subset=["text"])
    df = df.drop(["text"], axis=1)

    classes = list(df.columns.values[3:-2])
    schedule = Counter()

    # Ustalamy rozkład przynajleżności do poszczególnych klas
    for _, row in df.iterrows():
        c = classes[np.array(row[classes]).argmax()]
        schedule[c] += 1

    # Szukamy klas, które wystąpiły tylko raz
    onlyOnce = []
    rev = reversed(schedule.most_common())
    for item in rev:
        if item[1] == 1:
            onlyOnce.append(item[0])

    # Usuwamy te klasy, które wystąpiły tylko raz
    for item in onlyOnce:
        classes.remove(item)
    df = df.drop(columns=onlyOnce)

    row_test = []
    row_test_c = Counter()

    for cc, row in df.iterrows():
        c = classes[np.array(row[classes]).argmax()]
        if row[c] == 1:
            if row_test_c[c] < int(0.3*schedule[c])+1:
                row_test_c[c] += 1
                row_test.append(cc)

    test = pd.DataFrame()
    for row in row_test:
        test = test.append(df.loc[row])
    test[classes] = test[classes].astype(int)
    test["position"] = test["position"].astype(int)

    train = pd.DataFrame()
    for row in range(len(df)):
        if row not in row_test:
            train = train.append(df.iloc[row])
    train[classes] = train[classes].astype(int)
    train["position"] = train["position"].astype(int)

    test.to_csv("test_p.csv", index=False)
    train.to_csv("train_p.csv", index=False)
