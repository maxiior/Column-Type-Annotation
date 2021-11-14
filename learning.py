import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
# from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
import lime
from lime import lime_text
from sklearn.pipeline import make_pipeline
from lime.lime_text import LimeTextExplainer
import csv

trainds = pd.read_csv('train_p.csv')
testds = pd.read_csv('test_p.csv')

trainds = trainds.fillna('')
testds = testds.fillna('')

# Wyjmujemy wszystkie nazwy kategorii
classes = list(trainds.columns.values[3:-2])
classessm = [item.replace('http://dbpedia.org/ontology/', '')
             for item in classes]

# Vectorizer - przekształcenie danych tekstowych na wektory 600-składowe, z ngramami między 1, a 5 na podstawie TF-IDF
vectorizer = TfidfVectorizer(max_features=1000, lowercase=True,
                             analyzer='word', ngram_range=(1, 5), max_df=0.5, min_df=1)

x_train = vectorizer.fit_transform(trainds['text_dbpedied'])
y_train = np.array([np.array(item).argmax()
                   for _, item in trainds[classes].iterrows()]).reshape(-1, 1)

x_test = vectorizer.transform(testds['text_dbpedied'])
y_test = np.array([np.array(item).argmax()
                  for _, item in testds[classes].iterrows()]).reshape(-1, 1)

rfc = RandomForestClassifier(n_estimators=33)
model = rfc.fit(x_train, y_train)
predictions = model.predict(x_test)

filecols = {}

owngtcsvs = set()
for i in range(len(testds)):
    testowe = testds.loc[i]
    owngtcsvs.add(testowe["csv"])


with open("answears.csv", encoding="utf8") as f:
    with open("CTA_Round1_gt_own.csv", "w", encoding="utf8") as f2:
        csvwriter = csv.writer(f2)
        csvreader = csv.reader(f)

        for line in csvreader:
            filecols[line[0]] = line[1]
            if line[0] in owngtcsvs:
                csvwriter.writerow(line)

with open("model_submission.csv", "w", encoding="utf8") as f:
    csvwriter = csv.writer(f)

    for i in range(len(testds)):
        testowe = testds.loc[i]
        vece = vectorizer.transform([testowe["text_dbpedied"]])
        gt = classes[np.array(testowe[classes]).argmax()]
        predictions = model.predict(vece)
        pred = classes[predictions[0]]

        line = [
            testowe["csv"],
            filecols[testowe["csv"]],
            pred
        ]
        csvwriter.writerow(line)
