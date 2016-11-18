import re
import time
import cPickle as pickle
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

class Weights(object):
    def __init__(self, index):
        self._lenghts = {}
        self._index = index
        self._weights = self._build()

    def _build(self):
        return {}

    def get_lengths(self):
        return self._lenghts

    def get_weight(self, field, term, doc):
        if (field, term, doc) in self._weights:
            return self._weights[(field, term, doc)]
        else:
            return 0

class NaiveWeights(Weights):
    def __init__(self, index):
        super(NaiveWeights, self).__init__(index)

    def _build(self):
        W = {}
        N = self._index.get_documents_number()

        for doc in xrange(N):
            self._lenghts[doc] = 0

        for term in self._index.get_terms():
            for field in self._index.get_fields():
                postings_list = self._index.get_postings(field, term)
                for (doc, freq) in postings_list:
                    W[(field, term, doc)] = 1
                    self._lenghts[doc] += 1

        return W

class TfIdf(Weights):
    def __init__(self, index, use_normalization=False):
        self._normalize = use_normalization
        super(TfIdf, self).__init__(index)

    def _build(self):
        W = {}
        N = self._index.get_documents_number()

        W_docs = {}
        for doc in xrange(N):
            W_docs[doc] = 0
            self._lenghts[doc] = 0

        for term in self._index.get_terms():
            for field in self._index.get_fields():
                postings_list = self._index.get_postings(field, term)
                n = len(postings_list)
                idf = np.log10(np.true_divide(N, n))
                for (doc, freq) in postings_list:
                    tf = 1 + np.log10(freq)
                    w = np.multiply(tf, idf)
                    W[(field, term, doc)] = w
                    W_docs[doc] += w
                    self._lenghts[doc] += 1

        if self._normalize:
            # Normalization of weights
            for term in self._index.get_terms():
                for field in self._index.get_fields():
                    postings_list = self._index.get_postings(field, term)
                    for (doc, _) in postings_list:
                        w = W[(field, term, doc)]
                        W[(field, term, doc)] = np.true_divide(w, np.sqrt(W_docs[doc]))

        return W

class Search(object):
    def __init__(self, index, tf_idf=True):
        self._STOPWORDS = set(stopwords.words("english"))
        self._stemmer = PorterStemmer()
        self._tf_idf = tf_idf
        self._index = index
        self._weights = TfIdf(index) if tf_idf else NaiveWeights(index)

    def _format_query(self, query):
    	letters_only = re.sub("[^a-zA-Z]", " ", query)
    	words = letters_only.lower().split()
    	meaningful_words = [self._stemmer.stem(w) for w in words if not w in STOPWORDS]
        freqs = Counter(meaningful_words)
        return freqs.items()

    def _compose_query(self, query):
        fields = self._index.get_fields()
        for f in fields:
            query[f] = self._format_query(query[f])
        return query

    def _compute_query_weights(self, query):
        W = {}
        N = self._index.get_documents_number()
        fields = self._index.get_fields()

        for f in fields:
            terms = query[f]
            for (t, freq) in terms:
                if self._tf_idf:
                    postings_list = self._index.get_postings(field, term)
                    n = len(postings_list)
                    idf = np.log10(np.true_divide(N, n))
                    tf = 1 + np.log10(freq)
                    W[(f, t)] = np.multiply(tf, idf)
                else:
                    W(f, t) = 1

        return W

    def _rank(self, query):
        query = self._compose_query(query)
        query_weights = self._compute_query_weights(query)
        fields = self._index.get_fields()
        N = self._index.get_documents_number()
        lenghts = self._weights.get_lengths()

        scores = {}
        for doc in xrange(N):
            scores[doc] = 0

        for f in fields:
            terms = query[f]
            for (t, _) in terms:
                w_q = query_weights[(f, t)]
                postings_list = self._index.get_postings(f, t)
                for (doc, _) in postings_list:
                    scores[doc] += np.multiply(w_q, self._weights.get_weight(f, t, doc))

        for doc in xrange(N):
            scores[doc] = np.true_divide(scores[doc], lenghts[doc])

        scores = sorted(scores.items(), key=lambda t: t[1], reverse=True)

        return scores

    def search(self, query):
        return self._rank(query)
