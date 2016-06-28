import csv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.svm
import numpy as np

d = {}
l = []
communal_stripped = []
anticommunal_stripped = []
communal = []
anticommunal = []
features=[]
s = set()
sum = 0
# X and y are the arrays passed to the svm
x = []
y = []


def load_dict(filename):
    """give me file name i will load ur tweets into d[tweet text] = 0/1/2"""
    global l
    with open(filename, encoding='utf-8') as tsvfile:
        for line in csv.reader(tsvfile, dialect="excel-tab"):
            line[3] = re.sub('^RT @([a-zA-Z_0-9]*):', '', line[3])
            l.append(line[3])
            d[line[3]] = int(line[7])
            l = list(set(l))


def write_file(filename, type):
    writer = csv.writer(open(filename, 'w'), dialect="excel-tab")
    for key, value in d.items():
        if value == type:
            writer.writerow([key])
            if type == 1:
                communal.append(key)
            else:
                if type == 2:
                    anticommunal.append(key)


def vectorize():
    """"will convert the tweets into vector array of features,create x and y for the svm """
    global features
    temp = []
    with open('Communal.txt', 'r') as comm:
        for f in comm.read().split('\n'):
            if f != '':
                features.append(f)
    with open('AntiCommunal.txt', 'r') as anticomm:
        for f in anticomm.read().split('\n'):
            if f != '':
                features.append(f)
    for tweet in communal:
        temp = []
        for feature in features:
            if tweet.lower().find(feature.lower()) != -1:
                temp.append(1)
            else:
                temp.append(0)
        x.append(temp)
        y.append(1)
    for tweet in anticommunal:
        temp = []
        for feature in features:
            if tweet.lower().find(feature.lower()) != -1:
                temp.append(1)
            else:
                temp.append(0)
        x.append(temp)
        y.append(2)


if __name__ == '__main__':
    load_dict("nepal.tsv")
    load_dict("gurudaspur.tsv")
    load_dict("kashmir.tsv")

    write_file("communal.tsv", 1)
    write_file("anti_communal.tsv", 2)

    for i in range(0, 80):
        communal_stripped.append(communal[i])
    for i in range(0, 80):
        anticommunal_stripped.append(anticommunal[i])

    for key in d.keys():
            print(key, "->", d[key])

    print(len(l))
    # use this data only if u want to automatically extract features or else construct ur own vector using vectorize function written
    vectorizer = CountVectorizer(stop_words='english', min_df=0.053)
    data = vectorizer.fit_transform(communal_stripped + anticommunal)
    for t in data.toarray():
        print(t)
    # now we will generate the y vector 1 for communal and 2 for anticommunal
    for dummy in communal_stripped:
        y.append(1)
    for dummy in anticommunal:
        y.append(2)
    #please dont call vectorize if u r going to use data
    #vectorize()
    #print(features)
    #print(x)
    clf = sklearn.svm.SVC()
    clf.fit(data.toarray(), y)
    print(vectorizer.get_feature_names())

    print(clf.predict(data.toarray()[5]))
    #print(clf.predict(o))
    print(clf.predict(data.toarray()[120]))







