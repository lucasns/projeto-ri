import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Tokenizer(object):
    def __init__(self, use_stemming, remove_stopwords):
        self.use_stemming = use_stemming
        self.remove_stopwords = remove_stopwords
        self._STOPWORDS = set(stopwords.words("english"))
        self._stemmer = PorterStemmer()

    def _filter_words(self, words):
        if self.remove_stopwords:
            words = [w for w in words if not w in self._STOPWORDS]

        if self.use_stemming:
            words = [self._stemmer.stem(w) for w in words]

        return words

    def tokenize(self, query):
        letters_only = re.sub("[^a-zA-Z0-9]", " ", query)
        words = letters_only.lower().split()
        meaningful_words = self._filter_words(words)
        return meaningful_words
