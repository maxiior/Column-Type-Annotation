import pandas as pd
import numpy as np
from collections import Counter

def create_train_test_dataset():
    df = pd.read_csv("dataset_dbpedied.csv")
    df = df.drop_duplicates(subset=["text"])

    classes = list(df.columns.values[3:-1])
    rozklad = Counter()

    # Ustalamy rozkład przynajleżności do poszczególnych klas
    for cc, row in df.iterrows():
        c = classes[np.array(row[classes]).argmax()]
        rozklad[c] += 1

    # Szukamy klas, które wystąpiły tylko raz
    onlyOnce = []
    rev = reversed(rozklad.most_common())
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
            if row_test_c[c] < int(0.2*rozklad[c])+1:
                row_test_c[c] += 1
                row_test.append(cc)


    testds = pd.DataFrame()
    for row in row_test:
        testds = testds.append(df.loc[row])
    testds = testds.drop(columns=["Unnamed: 0"])
    testds[classes] = testds[classes].astype(int)

    trainds = pd.DataFrame()
    for row in range(len(df)):
        if row not in row_test:
            trainds = trainds.append(df.iloc[row])
    trainds = trainds.drop(columns=["Unnamed: 0"])
    trainds[classes] = trainds[classes].astype(int)

    testds.to_csv("test_p.csv")
    trainds.to_csv("train_p.csv")