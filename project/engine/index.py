import cPickle as pickle
from collections import OrderedDict

from tokenizer import Tokenizer


class MatrixTD(object):
    def __init__(self, use_stemming=True, remove_stopwords=True):
        self._tokenizer = Tokenizer(use_stemming, remove_stopwords)

    def _extract_terms(self, documents):
        terms = []
        for doc_id, info in documents.iteritems():
            for field in info.iterkeys():
                if info[field]:
                    words = self._tokenizer.tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, doc_id)
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def create_matrix(self, documents):
        terms = self._extract_terms(documents)
        matrix = OrderedDict()
        for term, doc_id in terms:
            matrix[term] = [0] * len(documents)
    
        for term, doc_id in terms:
            matrix[term][id-1] = 1

        return matrix


class BasicIndex(object):
    def __init__(self, use_compression, use_stemming=True, remove_stopwords=True):
        self.use_compression = use_compression
        self._tokenizer = Tokenizer(use_stemming, remove_stopwords)

    def _extract_terms(self, documents=True):
        terms = []
        for doc_id, info in documents.iteritems():
            for field in info.iterkeys():
                if info[field]:
                    words = self._tokenizer.tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, doc_id)
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
        for term, doc_id in terms:
            index.setdefault(term, []).append(doc_id)

        if self.use_compression:
            for term, post in index.iteritems():
                index[term] = self._compress_postings(post)
 
        return index


class FrequencyIndex(object):
    def __init__(self, use_compression=True, use_stemming=True, remove_stopwords=True):
        self.use_compression = use_compression
        self._tokenizer = Tokenizer(use_stemming, remove_stopwords)

    def _extract_terms(self, documents):
        terms = []
        for doc_id, info in documents.iteritems():
            for field in info.iterkeys():
                if info[field]:
                    words = self._tokenizer.tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, (doc_id, words.count(word)))
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def _compress_postings(self, postings):
        compressed = [postings[0]]

        last, _ = postings[0]
    
        for i in xrange(1, len(postings)):
            doc_id, freq = postings[i]
            new = (doc_id - last, freq)
            compressed.append(new)
            last = doc_id
    
        return compressed

    def create_index(self, documents):
        terms = self._extract_terms(documents)

        index = OrderedDict()
        for term, doc_id in terms:
            index.setdefault(term, []).append(doc_id)

        if self.use_compression:
            for term, post in index.iteritems():
                index[term] = self._compress_postings(post)
 
        return index


class PositionalIndex(object):
    def __init__(self, use_compression=True, use_stemming=True, remove_stopwords=True):
        self.use_compression = use_compression
        self._tokenizer = Tokenizer(use_stemming, remove_stopwords)

    def _indices(self, tokens, word):
        return [i for i, x in enumerate(tokens) if x == word]

    def _extract_terms(self, documents):
        terms = []
        for doc_id, info in documents.iteritems():
            for field in info.iterkeys():
                if info[field]:
                    words = self._tokenizer.tokenize(info[field])
                    for word in words:
                        full_word = word + '.' + field
                        pair = (full_word, (doc_id, words.count(word), self._indices(words, word)))
                        if pair not in terms:
                            terms.append(pair)

        return sorted(terms)

    def _compress_postings(self, postings):
        compressed = [postings[0]]

        last, _, _ = postings[0]
    
        for i in xrange(1, len(postings)):
            doc_id, freq, pos = postings[i]
            new = (doc_id - last, freq, pos)
            compressed.append(new)
            last = doc_id
    
        return compressed

    def create_index(self, documents):
        terms = self._extract_terms(documents)

        index = OrderedDict()
        for term, doc_id in terms:
            index.setdefault(term, []).append(doc_id)

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
        if not postings:
            return []

        dec_postings = [postings[0]]
        last, _ = postings[0]
        
        for i in xrange(1, len(postings)):
            curr, freq = postings[i]
            dec_postings.append((curr + last, freq))
            last += curr

        return dec_postings

    def _unique(self, seq):
        seen = set()
        return [x for x in seq if x not in seen and not seen.add(x)]
    
    def get_terms(self):
        terms = (k.split('.')[0] for k in self._index.iterkeys())
        return self._unique(terms)

    def get_fields(self):
        fields = (k.split('.')[1] for k in self._index.iterkeys())
        return self._unique(fields)
    
    def get_documents_number(self):
        return self._number_documents

    def get_postings(self, field, term):
        key = term + '.' + field
        return self._decompress(self._index.get(key, []))
