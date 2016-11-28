import cPickle as pickle
from collections import OrderedDict
import os

from classifier.classifier import Classifier
from crawler.crawler import crawl_domain
from wrapper.wrapper import Wrapper, MovieInfo
from engine.index import IndexWriter
import utils
import consts


def download_pages(out_path):
    crawl_domain(True, out_path)


def classify_pages(in_path, out_path):
    classifier = Classifier()

    with open(out_path, 'wb') as f:
        for site, html in utils.read_file_multiple(in_path):
            if classifier.classify(html):
                pickle.dump((site, html), f)


def extract_all_info(in_path, out_path, extract_type='specific'):
    wrapper = Wrapper()

    if extract_type == 'generic':
        extract_funtion = wrapper.extract_generic
    else:
        extract_funtion = wrapper.extract_specific

    info_list = []
    for site, html in utils.read_file_multiple(in_path):
        info = extract_funtion(html, site)
        if info.title is not None:  #Exclude movies without title
            info_list.append(info)
    
    with open(out_path, 'wb') as f:
        pickle.dump(info_list, f, pickle.HIGHEST_PROTOCOL)


def _format_runtime(site, runtime):
    min_format = ['rottentomatoes', 'metacritic', 'allmovie', 'tribute']
    hr_format = ['flixster', 'movies', 'imdb', 'boxofficemojo']
    
    converted = None
                
    if site in min_format:
        converted = utils.convert_min(runtime)
    elif site in hr_format:
        time = utils.convert_hr_min(runtime)
        converted = time if time > 0 else None
    elif site == "yify":
        full_time = utils.convert_hr_min_sec(runtime)
        min_time = utils.convert_min(runtime)

        if full_time > 0:
            converted = full_time
        elif min_time > 0:
            converted = min_time
        else:
            converted = None
    else:
        converted = runtime

    return converted


def _create_document(info, attributes):
    info = info._asdict()
    doc = OrderedDict()
    
    doc['site'] = info['site']

    for attr in attributes:
        if info[attr] is not None:
            if attr == 'genre' or attr == 'director':
                doc[attr] = ', '.join(info[attr])
            elif attr == 'date':
                year = utils.convert_date(info['date'])[2]
                doc['date'] = year if year is not None else None
            elif attr == 'runtime':
                doc['runtime'] = str(_format_runtime(info['site'], info['runtime']))
            else:
                doc[attr] = info[attr]
        else:
            doc[attr] = ""  # Substitute None for empty strings

    return doc


def create_documents(in_path, out_path):
    attributes = ['title', 'genre', 'director', 'date', 'runtime']

    documents = OrderedDict()

    for id, info in enumerate(utils.read_file(in_path), 1):
        documents[id] = _create_document(info, attributes)
    
    print documents
    with open(out_path, 'wb') as f:
        pickle.dump(documents, f)


def create_index(in_path, out_path):
    writer = IndexWriter()
    documents = utils.read_file(in_path)
    for doc in documents.itervalues():
        doc.pop('site', None)

    writer.write_index(documents, out_path)


def create_data():
    if not os.path.exists(consts.DATA_DIR):
        os.makedirs(consts.DATA_DIR)

    if not os.path.exists(consts.CRAWLED_PATH):
        download_pages(consts.CRAWLED_PATH)

    if not os.path.exists(consts.CLASSIFIED_PATH):
        classify_pages(consts.CRAWLED_PATH, consts.CLASSIFIED_PATH)

    if not os.path.exists(consts.EXTRACTED_PATH):
        extract_all_info(consts.CLASSIFIED_PATH, consts.EXTRACTED_PATH)

    if not os.path.exists(consts.DOCUMENTS_PATH):
        create_documents(consts.EXTRACTED_PATH, consts.DOCUMENTS_PATH)

    if not os.path.exists(consts.INDEX_PATH):
        create_index(consts.DOCUMENTS_PATH, consts.INDEX_PATH)


if __name__ == '__main__':
    create_data()
