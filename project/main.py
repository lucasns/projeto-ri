from engine.index import IndexReader
from engine.search import Search

import utils
import consts


SEARCHER = Search(IndexReader(consts.INDEX_PATH))


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


def main():
    print "Consulta:"
    title = raw_input("Title: ")
    genre = raw_input("Genre: ")
    director = raw_input("Director: ")
    date = raw_input("Date (Year): ")
    runtime = int(raw_input("Runtime:\n0 - 0-1 hr\n1 - 1-2 hr\n2 - 2-3 hr\n3 - More than 4 hr\n4 - ANY\n"))

    if runtime >= 0 and runtime < 4:
        runtime = utils.MovieTime(runtime * 60 + 1).quartile()
    else:
        runtime = ""

    query = {}
    query['title'] = title
    query['genre'] = genre
    query['director'] = director
    query['date'] = date
    query['runtime'] = runtime

    print
    for doc in search(query):
        for k, v in doc.iteritems():
            print k, ": ", v
        print


if __name__ == '__main__':
    main()
