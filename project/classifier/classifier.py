import cPickle as pickle
from time import time
from tools import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB

class Classifier(Object):
    def __init__(self):
        self._classifier = None
        self._database = load_database()
        self._X, self._Y = prepare_database(self._database)

        self._vocabulary = None # Create bag of words or TF-IDF model
        self._features_train, self._features_test, self._labels_train, self._labels_test = split_dataset(self._vocabulary, self._Y)

    def classify(html):
        text = extract_text(html)
        X = self._vocabulary.transform([text])
        y = self._classifier.predict(X)[0]
        return y
