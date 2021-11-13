import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv("glove_df_dbpedied_p.csv")
df = df.drop_duplicates(subset=["text"])

classes = list(df.columns.values[3:-1])

print(len(classes))
input()

rozklad = Counter()

# Ustalamy rozkład przynajleżności do poszczególnych klas
for cc, row in df.iterrows():
    cat = classes[np.array(row[classes]).argmax()]
    rozklad[cat] += 1

# Szukamy klas, które wystąpiły tylko raz
theonly = []
rev = reversed(rozklad.most_common())
for item in rev:
    if item[1] == 1:
        theonly.append(item[0])

# Usuwamy te klasy, które wystąpiły tylko raz
for item in theonly:
    classes.remove(item)
df = df.drop(columns=theonly)

row_test = []
row_test_cats = Counter()

for cc, row in df.iterrows():
    cat = classes[np.array(row[classes]).argmax()]

    if row[cat] == 1:
        if row_test_cats[cat] < int(0.2*rozklad[cat])+1:
            row_test_cats[cat] += 1
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
