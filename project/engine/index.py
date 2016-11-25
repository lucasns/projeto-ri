import os
import cPickle as pickle
from collections import OrderedDict
import re

from stemming.porter2 import stem
from stop_words import get_stop_words


def tokenize(str):
    stop_words = get_stop_words('english')
    letters_only = re.sub("[^a-zA-Z\-]", " ", str)
    words = letters_only.lower().split()
    words = [w for w in words if not w in stop_words]
    words = [stem(w) for w in words]
    return words


class MatrixTD(object):
    def _extract_terms(self, documents):
        terms = []
        for id, info in enumerate(documents, 1):
            for field in info.iterkeys():
                if info[field]:
                    words = tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, id)
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def create_matrix(self, documents):
        terms = self._extract_terms(documents)
        matrix = OrderedDict()
        for term, id in terms:
            matrix[term] = [0] * len(documents)
    
        for term, id in terms:
            matrix[term][id-1] = 1

        return matrix


class BasicIndex(object):
    def __init__(self, use_compression):
        self.use_compression = use_compression

    def _extract_terms(self, documents=True):
        terms = []
        for id, info in enumerate(documents, 1):
            for field in info.iterkeys():
                if info[field]:
                    words = tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, id)
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def _compress_postings(self, postings):
        last = postings[0]
        compressed = [last]
    
        for i in xrange(1, len(postings)):
            new = postings[i] - last
            compressed.append(new)
            last = postings[i]
    
        return compressed

    def create_index(self, documents):
        terms = self._extract_terms(documents)

        index = OrderedDict()
        for term, id in terms:
            index.setdefault(term, []).append(id)

        if self.use_compression:
            for term, post in index.iteritems():
                index[term] = self._compress_postings(post)
 
        return index


class FrequencyIndex(object):
    def __init__(self, use_compression=True):
        self.use_compression = use_compression

    def _extract_terms(self, documents):
        terms = []
        for id, info in enumerate(documents, 1):
            for field in info.iterkeys():
                if info[field]:
                    words = tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, (id, words.count(word)))
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def _compress_postings(self, postings):
        compressed = [postings[0]]

        last, _ = postings[0]
    
        for i in xrange(1, len(postings)):
            id, freq = postings[i]
            new = (id - last, freq)
            compressed.append(new)
            last = id
    
        return compressed

    def create_index(self, documents):
        terms = self._extract_terms(documents)

        index = OrderedDict()
        for term, id in terms:
            index.setdefault(term, []).append(id)

        if self.use_compression:
            for term, post in index.iteritems():
                index[term] = self._compress_postings(post)
 
        return index


class PositionalIndex(object):
    def __init__(self, use_compression=True):
        self.use_compression = use_compression

    def _indices(self, tokens, word):
        return [i for i, x in enumerate(tokens) if x == word]

    def _extract_terms(self, documents):
        terms = []
        for id, info in enumerate(documents, 1):
            for field in info.iterkeys():
                if info[field]:
                    words = tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, (id, words.count(word), self._indices(words, word)))
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def _compress_postings(self, postings):
        compressed = [postings[0]]

        last, _, _ = postings[0]
    
        for i in xrange(1, len(postings)):
            id, freq, pos = postings[i]
            new = (id - last, freq, pos)
            compressed.append(new)
            last = id
    
        return compressed

    def create_index(self, documents):
        terms = self._extract_terms(documents)

        index = OrderedDict()
        for term, id in terms:
            index.setdefault(term, []).append(id)

        if self.use_compression:
            for term, post in index.iteritems():
                index[term] = self._compress_postings(post)
 
        return index


class IndexWriter(object):
    def __init__(self, use_compression=True):
        self._index_type = FrequencyIndex(use_compression)

    def write_index(self, documents, file_path):
        index = self._index_type.create_index(documents)
        with open(file_path, 'wb') as f:
            pickle.dump((len(documents), index), f, pickle.HIGHEST_PROTOCOL)

        
class IndexReader(object):
    def __init__(self, index):
        self._index = index[1]
        self._number_documents = index[0]

    def _decompress(self, postings):
        dec_postings = [postings[0]]
        last, _ = postings[0]
        
        for i in xrange(1, len(postings)):
            curr, freq = postings[i]
            dec_postings.append((curr + last, freq))
            last += curr

        return dec_postings
    
    def get_terms(self):
        return [k.split('.')[0] for k in self._index.iterkeys()]

    def get_fields(self):
        return [k.split('.')[1] for k in self._index.iterkeys()]
    
    def get_documents_number(self):
        return self._number_documents

    def get_postings(self, field, term):
        key = term + '.' + field
        return self._decompress(self._index[key])
