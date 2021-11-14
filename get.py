import pandas as pd

MAX_FILE_SIZE = 50

file_names = pd.DataFrame(columns=['names', 'position'])

df = pd.read_csv("CTA_DBP_Round1_Targets.csv")

for i in df.iloc:
    file_names = file_names.append(
        {'names': i[0], 'position': i[1]}, ignore_index=True)

classes_that_work = []

f = open("classes_that_work.txt", "r")
for i in f:
    classes_that_work.append(i.replace('\n', '').lower())
f.close()

definitive_files = pd.DataFrame(columns=['names', 'position'])

for i in file_names.iloc:
    df = pd.read_csv('tables\\' + i[0] + ".csv")
    q = 0
    for j in df[df.columns.tolist()[0]]:
        q += 1
    if q < MAX_FILE_SIZE:
        for j in df.columns:
            if df.columns.tolist().index(j) == i[1] and j.lower() in classes_that_work:
                definitive_files = definitive_files.append(
                    {'names': i.iloc[0], 'position': i.iloc[1]}, ignore_index=True)
definitive_files.to_csv("CTA_DBP_Round1_Targets.csv", index=False)

#definitive_files = list(dict.fromkeys(definitive_files))

columns = ['csv', 'text']
for i in classes_that_work:
    columns.append('http://dbpedia.org/ontology/' + i)

q = 0
for i in definitive_files.iloc:
    q += 1
print(q)

df = pd.DataFrame(columns=columns)

for i in definitive_files.iloc:
    csv = pd.read_csv("tables\\" + i[0] + ".csv")

    s = ""

    for k, j in enumerate(csv[csv.columns.tolist()[i[1]]]):
        if k == len(csv[csv.columns.tolist()[i[1]]]) - 1:
            s += "\"" + str(j) + "\""
        else:
            s += "\"" + str(j) + "\";"

    classes = {'csv': i[0], 'text': s}

    for j in classes_that_work:
        if j in [i.lower() for i in csv.columns.tolist()]:
            if i[1] == [i.lower() for i in csv.columns.tolist()].index(j):
                classes['http://dbpedia.org/ontology/'+j] = 1
            else:
                classes['http://dbpedia.org/ontology/'+j] = 0
        else:
            classes['http://dbpedia.org/ontology/'+j] = 0

    df = df.append(classes, ignore_index=True)

df.to_csv("glove.csv", index=False)
