from engine.index import IndexReader
from engine.search import Search
from interface import Interface

import utils
import consts

 
INDEX_READER = IndexReader(consts.INDEX_PATH)
SEARCHER = Search(INDEX_READER)


def get_documents(id_list):
    '''list of ids -> list of documents'''
    documents = utils.read_file(consts.DOCUMENTS_PATH)

    docs_list = []
    for doc_id in id_list:
        docs_list.append(documents[doc_id])

    return docs_list


def search(query):
    '''query -> list of documents'''
    hits = SEARCHER.search(query)
    ids = [doc_id for doc_id, rank in hits]
    return get_documents(ids)


def run():
	while True:
	    interface = Interface(INDEX_READER.get_fields())
	    query = interface._get_query_from_user()

	    documents_list = search(query)
	    interface._show_retrieved_documents(documents_list)

if __name__ == '__main__':
    run()