import csv
import os
import cPickle as pickle
from time import time

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

import tools


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RESULTS_PATH = os.path.join(DIR_PATH, 'results')


def list_scores(scores):
    res = [scores['accuracy'], scores['precision'], scores['recall'], scores['f1']]
    return res


def try_svm(features_train, features_test, labels_train, labels_test):
    C = [1, 10, 20, 100, 1000, 10000]
    kernels = ['rbf', 'linear', 'poly', 'sigmoid']

    rows = []

    for c in C:
        for kernel in kernels:
            alg_name = "SVM (C=%d, kernel=%s)" % (c, kernel)

            t0 = time()
            clf = SVC(C=c, kernel=kernel)
            clf.fit(features_train, labels_train)
            training_time = "%fs" % round(time() - t0, 3)

            scores = tools.evaluate(labels_test, clf.predict(features_test))

            rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_random_forest(features_train, features_test, labels_train, labels_test):
    N = [10, 20, 100, 200, 300, 10000]

    rows = []

    for n in N:
        alg_name = "Random Forest (N=%d)" % n

        t0 = time()
        clf = RandomForestClassifier(n_estimators = n)
        clf.fit(features_train, labels_train)
        training_time = "%fs" % round(time() - t0, 3)

        scores = tools.evaluate(labels_test, clf.predict(features_test))
        rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_regression(features_train, features_test, labels_train, labels_test):
    alg_name = "Linear Regression"

    t0 = time()
    clf = LinearRegression()
    clf.fit(features_train, labels_train)
    training_time = "%fs" % round(time() - t0, 3)

    rows = [[alg_name, training_time, clf.score(features_train, labels_train), "", "", ""]]

    return rows


def try_naive_bayes(features_train, features_test, labels_train, labels_test):
    alg_name = "Naive Bayes"

    t0 = time()
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    training_time = "%fs" % round(time() - t0, 3)

    scores = tools.evaluate(labels_test, clf.predict(features_test))

    rows = [[alg_name, training_time] + list_scores(scores)]

    return rows


def try_ada_boost(features_train, features_test, labels_train, labels_test):
    N = [1, 5, 10, 30, 40, 100, 1000]
    R = [0.1, 0.5, 0.7, 0.8, 0.9, 1]

    rows = []

    for n in N:
        for lr in R:
            alg_name = "AdaBoost (N=%d, learning_rate=%f)" % (n, lr)

            t0 = time()
            clf = AdaBoostClassifier(n_estimators=n, learning_rate=lr)
            clf.fit(features_train, labels_train)
            training_time = "%fs" % round(time() - t0, 3)

            scores = tools.evaluate(labels_test, clf.predict(features_test))

            rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_knn(features_train, features_test, labels_train, labels_test):
    N = [1, 5, 10, 20, 30, 35, 40]

    rows = []

    for n in N:
        alg_name = "k-NN (k=%d)" % n

        t0 = time()
        clf = KNeighborsClassifier(n_neighbors=n)
        clf.fit(features_train, labels_train)
        training_time = "%fs" % round(time() - t0, 3)

        scores = tools.evaluate(labels_test, clf.predict(features_test))
        rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def save_csv(filename, rows):
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)

    filename = os.path.join(RESULTS_PATH, filename+'.csv')
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def compare_classifiers():
    db = tools.load_database()
    X, Y = tools.prepare_database(db)

    bag_of_words, bag_of_words_vectors = tools.create_bag_of_words(X)
    tfidf, tfidf_vectors = tools.create_TfIdf(X)

    print "Testing Bag of Words"

    filename = "bag-of-words-results"
    rows = [['Algorithm', 'Training Time', 'Accuracy', 'Precision', 'Recall', 'F1-Measure']]

    features_train, features_test, labels_train, labels_test = tools.split_dataset(bag_of_words_vectors, Y)

    rows += try_naive_bayes(features_train, features_test, labels_train, labels_test)
    rows += try_regression(features_train, features_test, labels_train, labels_test)
    rows += try_random_forest(features_train, features_test, labels_train, labels_test)
    rows += try_svm(features_train, features_test, labels_train, labels_test)
    rows += try_ada_boost(features_train, features_test, labels_train, labels_test)
    rows += try_knn(features_train, features_test, labels_train, labels_test)

    save_csv(filename, rows)

    print "Testing TF-IDF"

    filename = "tf-idf-results"
    rows = [['Algorithm', 'Training Time', 'Accuracy', 'Precision', 'Recall', 'F1-Measure']]

    features_train, features_test, labels_train, labels_test = tools.split_dataset(tfidf_vectors, Y)

    rows += try_naive_bayes(features_train, features_test, labels_train, labels_test)
    rows += try_regression(features_train, features_test, labels_train, labels_test)
    rows += try_random_forest(features_train, features_test, labels_train, labels_test)
    rows += try_svm(features_train, features_test, labels_train, labels_test)
    rows += try_ada_boost(features_train, features_test, labels_train, labels_test)
    rows += try_knn(features_train, features_test, labels_train, labels_test)

    save_csv(filename, rows)


if __name__ == "__main__":
    compare_classifiers()
