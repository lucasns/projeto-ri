import cPickle as pickle
from time import time
from tools import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

class Classifier(object):
    def __init__(self):
        self._classifier = None # Need to define which classifier will be used
        self._database = load_database()
        self._X, self._Y = prepare_database(self._database)

        self._vocabulary = None # Create bag of words or TF-IDF model
        self._features_train, self._features_test, self._labels_train, self._labels_test = split_dataset(self._vocabulary, self._Y)

        self._classifier.fit(self._features_train, self._labels_train)
        self._scores = evaluate(self._labels_test, self._classifier.predict(self._features_test))
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

    def classify(self, html):
        text = extract_text(html)
        X = self._vocabulary.transform([text])
        y = self._classifier.predict(X)[0]
        return y

    def get_scores(self):
        return self._scores
