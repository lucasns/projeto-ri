import cPickle as pickle
import os

from classifier.classifier import Classifier
from crawler.crawler import crawl_domain
from wrapper.wrapper import Wrapper, MovieInfo
from utils import read_file, read_file_multiple
from consts import CRAWLED_PAGES_PATH, CLASSIFIED_PAGES_PATH, EXTRACTED_INFO_PATH, DOCUMENTS_PATH, INDEX_PATH, DATA_DIR


def download_pages(out_path):
    crawl_domain(True, out_path)


def classify_pages(in_path, out_path):
    classifier = Classifier()

    with open(out_path, 'wb') as f:
        for site, html in read_file_multiple(in_path):
            if classifier.classify(html):
                pickle.dump((site, html), f)


def extract_all_info(in_path, out_path, extract_type='specific'):
    wrapper = Wrapper()

    if extract_type == 'generic':
        extract_funtion = wrapper.extract_generic
    else:
        extract_funtion = wrapper.extract_specific
    
    with open(out_path, 'wb') as f:
        for site, html in read_file_multiple(in_path):
            info = extract_funtion(html, site)
            pickle.dump(info, f, pickle.HIGHEST_PROTOCOL)


def create_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(CRAWLED_PAGES_PATH):
        download_pages(CRAWLED_PAGES_PATH)

    if not os.path.exists(CRAWLED_PAGES_PATH):
        classify_pages(CRAWLED_PAGES_PATH, CLASSIFIED_PAGES_PATH)

    if not os.path.exists(CRAWLED_PAGES_PATH):
        extract_all_info(CLASSIFIED_PAGES_PATH, EXTRACTED_INFO_PATH)


if __name__ == '__main__':
    create_data()
