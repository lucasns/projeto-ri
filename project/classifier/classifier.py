from sklearn.ensemble import AdaBoostClassifier

import tools


class Classifier(object):
    def __init__(self):
        self._classifier = AdaBoostClassifier(n_estimators=1000, learning_rate=0.5) # Best classifier
        self._database = tools.load_database()
        self._X, self._Y = tools.prepare_database(self._database)

        self._vocabulary, self._vocabulary_vectors = tools.create_bag_of_words(self._X) # Creates Bag of Words model
        self._features_train, self._features_test, self._labels_train, self._labels_test = tools.split_dataset(self._vocabulary_vectors, self._Y)

        self._classifier.fit(self._features_train, self._labels_train)
        self._scores = tools.evaluate(self._labels_test, self._classifier.predict(self._features_test))

    def classify(self, html):
        text = tools.extract_text(html)
        X = self._vocabulary.transform([text])
        y = self._classifier.predict(X)[0]
        return y

    def get_scores(self):
        return self._scores


def _test():
    import urllib2

    USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    url = 'https://www.rottentomatoes.com/m/tideland'
    page = urllib2.Request(url, headers=USER_AGENT)
    page = urllib2.urlopen(page)
    html_text = page.read()

    clf = Classifier()
    scores = clf.get_scores()
    result = 'Is relevant' if clf.classify(html_text) == 1 else 'Is not relevant'

    print "Accuracy: %f" % scores['accuracy']
    print "Precision: %f" % scores['precision']
    print "Recall: %f" % scores['recall']
    print "F1-Measure: %f" % scores['f1']

    print "\nResult for url %s: '%s'" % (url, result)

if __name__ == '__main__':
    _test()
