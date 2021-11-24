import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import csv
import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action='ignore', category=DataConversionWarning)


def train_and_test_process():
    trainds = pd.read_csv('train_p.csv')
    testds = pd.read_csv('test_p.csv')

    trainds = trainds.fillna('')
    testds = testds.fillna('')

    # Wyjmujemy wszystkie nazwy kategorii
    classes = list(trainds.columns.values[1:-2])

    # Vectorizer - przekształcenie danych tekstowych na wektory 600-składowe, z ngramami między 1, a 5 na podstawie TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000, lowercase=True,
                                 analyzer='word', ngram_range=(1, 5), max_df=0.5, min_df=1)

    x_train = vectorizer.fit_transform(trainds['text_dbpedied'])
    y_train = np.array([np.array(item).argmax()
                        for _, item in trainds[classes].iterrows()]).reshape(-1, 1)

    rfc = RandomForestClassifier()
    model = rfc.fit(x_train, y_train)

    print("train_and_test_process | Wyuczenie modelu: DONE")

    owngtcsvs = set()
    for i in range(len(testds)):
        testowe = testds.loc[i]
        owngtcsvs.add(testowe["csv"])

    with open("model_submission.csv", "w", encoding="utf8") as f:
        csvwriter = csv.writer(f)

        for i in range(len(testds)):
            testowe = testds.loc[i]
            vece = vectorizer.transform([testowe["text_dbpedied"]])
            predictions = model.predict(vece)
            pred = classes[predictions[0]]

            line = [
                testowe["csv"],
                testowe["position"],
                pred
            ]
            csvwriter.writerow(line)

    print("train_and_test_process | Wykonanie predykcji na zbiorze testowym: DONE")
    print("train_and_test_process | Utworzenie pliku model_submission.csv: DONE")