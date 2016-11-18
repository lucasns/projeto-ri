import os


#Directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, os.path.join(os.pardir, 'data'))
RESULTS_DIR = os.path.join(ROOT_DIR, os.path.join(os.pardir, 'results'))
INDEX_DIR = os.path.join(ROOT_DIR, os.path.join(os.pardir, 'index'))

#Files
CRAWLED_PAGES_PATH = os.path.join(DATA_DIR, 'crawled-pages.pickle')
CLASSIFIED_PAGES_PATH = os.path.join(DATA_DIR, 'classified-pages.pickle')
EXTRACTED_INFO_PATH = os.path.join(DATA_DIR, 'extracted-info.pickle')
DOCUMENTS_PATH = os.path.join(DATA_DIR, 'documents.pickle')
INDEX_PATH = os.path.join(INDEX_DIR, 'index.pickle')
