import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv("xxx.csv")
df = df.drop_duplicates(subset=["text"])

classes = list(df.columns.values[3:-1])

rozklad = Counter()

for cc, row in df.iterrows():
    cat = classes[np.array(row[classes]).argmax()]
    rozklad[cat] += 1

theonly = []
rev = reversed(rozklad.most_common())
for item in rev:
    if item[1] == 1:
        theonly.append(item[0])

for item in theonly:
    classes.remove(item)

df = df.drop(columns=theonly)

rowtest = []
rowtestcats = Counter()

for cc, row in df.iterrows():
    cat = classes[np.array(row[classes]).argmax()]

    if row[cat] == 1:
        if rowtestcats[cat] < int(0.2*rozklad[cat])+1:
            print(cc, cat)
            rowtestcats[cat] += 1
            rowtest.append(cc)


testds = pd.DataFrame()
for row in rowtest:
    testds = testds.append(df.loc[row])

testds = testds.drop(columns=["Unnamed: 0"])

testds[classes] = testds[classes].astype(int)
print(testds[classes])

trainds = pd.DataFrame()

for row in range(len(df)):
    if row not in rowtest:
        print(df.iloc[row])
        trainds = trainds.append(df.iloc[row])

trainds = trainds.drop(columns=["Unnamed: 0"])

trainds[classes] = trainds[classes].astype(int)

testds.to_csv("test_p.csv")
trainds.to_csv("train_p.csv")