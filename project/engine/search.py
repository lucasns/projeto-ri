import numpy as np
from tokenizer import Tokenizer
from collections import Counter

class Weights(object):
    def __init__(self, index_reader):
        self._lenghts = {}
        self._index_reader = index_reader
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
    def __init__(self, index_reader):
        super(NaiveWeights, self).__init__(index_reader)

    def _build(self):
        W = {}
        N = self._index_reader.get_documents_number()

        for doc in xrange(N):
            self._lenghts[doc] = 0

        for term in self._index_reader.get_terms():
            for field in self._index_reader.get_fields():
                postings_list = self._index_reader.get_postings(field, term)
                for (doc, freq) in postings_list:
                    W[(field, term, doc)] = 1
                    self._lenghts[doc] += 1

        return W


class TfIdf(Weights):
    def __init__(self, index_reader):
        super(TfIdf, self).__init__(index_reader)

    def _build(self):
        W = {}
        N = self._index_reader.get_documents_number()

        for doc in xrange(N):
            self._lenghts[doc] = 0

        for term in self._index_reader.get_terms():
            for field in self._index_reader.get_fields():
                postings_list = self._index_reader.get_postings(field, term)
                n = len(postings_list)
                if n != 0:
                    idf = np.log10(np.true_divide(N, n))
                    for (doc, freq) in postings_list:
                        tf = 1 + np.log10(freq)
                        w = np.multiply(tf, idf)
                        W[(field, term, doc)] = w
                        self._lenghts[doc] += 1

        return W


class Search(object):
    def __init__(self, index_reader, tf_idf=True):
        self._tokenizer = Tokenizer(use_stemming=True, remove_stopwords=True)
        self._tf_idf = tf_idf
        self._index_reader = index_reader
        self._weights = TfIdf(index_reader) if tf_idf else NaiveWeights(index_reader)

    def _format_query(self, query):
        meaningful_words = self._tokenizer.tokenize(query)
        freqs = Counter(meaningful_words)
        return freqs.items()

    def _compose_query(self, query):
        fields = self._index_reader.get_fields()
        for f in fields:
            if f in query:
                query[f] = self._format_query(query[f])
        return query

    def _compute_query_weights(self, query):
        W = {}
        N = self._index_reader.get_documents_number()
        fields = self._index_reader.get_fields()

        for f in fields:
            if f in query:
                terms = query[f]
                for (t, freq) in terms:
                    if self._tf_idf:
                        postings_list = self._index_reader.get_postings(f, t)
                        n = len(postings_list)
                        if n != 0:
                            idf = np.log10(np.true_divide(N, n))
                            tf = 1 + np.log10(freq)
                            W[(f, t)] = np.multiply(tf, idf)
                        else:
                            W[(f, t)] = 0
                    else:
                        W[(f, t)] = 1

        return W

    def _rank(self, query):
        query = self._compose_query(query)
        query_weights = self._compute_query_weights(query)
        fields = self._index_reader.get_fields()
        N = self._index_reader.get_documents_number()
        lenghts = self._weights.get_lengths()

        scores = {}
        for doc in xrange(N):
            scores[doc] = 0

        for f in fields:
            if f in query:
                terms = query[f]
                for (t, _) in terms:
                    w_q = query_weights[(f, t)]
                    postings_list = self._index_reader.get_postings(f, t)
                    for (doc, _) in postings_list:
                        scores[doc] += np.multiply(w_q, self._weights.get_weight(f, t, doc))

        for doc in xrange(N):
            scores[doc] = np.true_divide(scores[doc], lenghts[doc])

        scores = sorted(scores.items(), key=lambda t: t[1], reverse=True)

        return scores

    def search(self, query):
        return self._rank(query)
