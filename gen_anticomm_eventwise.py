import csv
import re
import sort_tweets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import cross_validation
from scipy.sparse import coo_matrix
from sklearn.utils import shuffle
import numpy as np
x = []
y = []


def make_balanced_set(x,y,rand):
    '''make a balanced set of general and anti-communal tweet in future split the returned data into train and test sets '''
    balanced_x=[]
    balanced_y=[]
    no_of_anticomm=0;
    x,y=shuffle(x,y,random_state=rand)
    for tweet,type in zip(x,y):
        if type == 2:
            balanced_x.append(tweet)
            balanced_y.append(type)
            no_of_anticomm += 1
    for tweet,type in zip(x, y):
        if type == 0 and no_of_anticomm > 0:
            balanced_x.append(tweet)
            balanced_y.append(type)
            no_of_anticomm -= 1
    return balanced_x,balanced_y

if __name__ == '__main__':
    sort_tweets.load_dict("California.tsv")
    for key in sort_tweets.d.keys():
        if sort_tweets.d[key] == 0 or sort_tweets.d[key]==2:
            x.append(key)
            y.append(sort_tweets.d[key])

    # start vectorizing text tweet use nltk.tokenize in future
    # rewrite x as a 2D array of vector
    vectorizer = CountVectorizer(stop_words='english')
    x = vectorizer.fit_transform(x)
    ##
    #change last argument to shuffle in a different way
    x, y = make_balanced_set(x.toarray(), y, 12)

    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(x,y,test_size=0.2,random_state=5)
    #change random state to make random shuffling
    skf = cross_validation.StratifiedShuffleSplit(y,n_iter=1,test_size=0.2, random_state=4)  # 2-fold cross validation

    for train_index, test_index in skf:
        #print(train_index)
        #print(test_index)
        X_train = [x[i] for i in train_index]
        y_train = [y[i] for i in train_index]
        X_test = [x[i] for i in test_index]
        y_test = [y[i] for i in test_index]

    print(y_train)
    print(y_test)

    gen=anticomm=0

    for tweet, t in zip(X_test, y_test):
        if t==0:
            gen+=1
        if t==2:
            anticomm+=1
    #print(gen,",",anticomm)

    clf = SVC(kernel='linear', C=1).fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("ACCURACY = ", score*100, "%")


