import cPickle as pickle
from time import time
from tools import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB

def print_scores(scores):
    print "Accuracy: %f" % scores['accuracy']
    print "Precision: %f" % scores['precision']
    print "Recall: %f" % scores['recall']
    print "F1-Measure: %f\n" % scores['f1']

def try_svm(features_train, features_test, labels_train, labels_test):
    print "Testing SVMs:\n-------------\n"

    C = [1, 10, 20, 100, 1000, 10000]
    kernels = ['rbf', 'linear', 'poly', 'sigmoid']

    for c in C:
        for kernel in kernels:
            print "C=%d, kernel=%s" % (c, kernel)

            t0 = time()
            clf = SVC(C=c, kernel=kernel)
            clf.fit(features_train, labels_train)
            print "Training time %fs" % round(time() - t0, 3)

            scores = evaluate(labels_test, clf.predict(features_test))
            print_scores(scores)

def try_random_forest(features_train, features_test, labels_train, labels_test):
    print "Testing Random Forests:\n-----------------------\n"

    N = [10, 20, 100, 200, 300, 10000]

    for n in N:
        print "N=%d" % n

        t0 = time()
        clf = RandomForestClassifier(n_estimators = n)
        clf.fit(features_train, labels_train)
        print "Training time %fs" % round(time() - t0, 3)

        scores = evaluate(labels_test, clf.predict(features_test))
        print_scores(scores)

def try_regression(features_train, features_test, labels_train, labels_test):
    print "Testing Linear Regression:\n--------------------------\n"

    t0 = time()
    clf = LinearRegression()
    clf.fit(features_train, labels_train)
    print "Training time %fs" % round(time() - t0, 3)

    print "Naive score %f" % clf.score(features_train, labels_train)
    print "R squared score %f\n" % clf.score(features_test, labels_test)

def try_naive_bayes(features_train, features_test, labels_train, labels_test):
    print "Testing Naive Bayes:\n--------------------\n"

    t0 = time()
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    print "Training time %fs" % round(time() - t0, 3)

    scores = evaluate(labels_test, clf.predict(features_test))
    print_scores(scores)

def try_ada_boost(features_train, features_test, labels_train, labels_test):
    #TODO
    pass

def try_knn(features_train, features_test, labels_train, labels_test):
    #TODO
    pass

def compare():
    db = load_database()
    X, Y = prepare_database(db)

    bag_of_words, bag_of_words_vectors = create_bag_of_words(X)
    tfidf, tfidf_vectors = create_TfIdf(X)

    print "\nUsing Bag of Words:\n===================\n"

    features_train, features_test, labels_train, labels_test = split_dataset(bag_of_words_vectors, Y)

    try_naive_bayes(features_train, features_test, labels_train, labels_test)
    try_regression(features_train, features_test, labels_train, labels_test)
    try_random_forest(features_train, features_test, labels_train, labels_test)
    try_svm(features_train, features_test, labels_train, labels_test)

    print "\nUsing TF-IDF:\n=============\n"

    features_train, features_test, labels_train, labels_test = split_dataset(tfidf_vectors, Y)

    try_naive_bayes(features_train, features_test, labels_train, labels_test)
    try_regression(features_train, features_test, labels_train, labels_test)
    try_random_forest(features_train, features_test, labels_train, labels_test)
    try_svm(features_train, features_test, labels_train, labels_test)

if __name__ == "__main__":
    compare()
