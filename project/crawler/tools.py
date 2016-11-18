import cPickle as pickle

from crawler import Crawler
from config import FILES_PATH


def export_all_crawled_pages(filename, delete_files=False):
    path = FILES_PATH

    results = {}

    for website_name in DOMAINS.keys():
        folder_path = os.path.join(path, website_name)

        if not os.path.exists(folder_path):
            continue

        results[website_name] = []

        for page in os.listdir(folder_path):
            f_name = os.path.join(folder_path, page)
            with open(f_name, 'r') as pagefile:
                results[website_name].append(pagefile.read())

            if delete_files:
                os.remove(f_name)

        if delete_files:
            os.rmdir(folder_path)

    with open(os.path.join(path, filename), 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)


def import_crawled_pages(filename):
    path = FILES_PATH
    filename = os.path.join(path, filename)

    results = {}
    with open(filename, 'rb') as f:
        results = pickle.load(f)
    return results


def crawl(use_heuristic, filename):
    crawlers = []
    for website_name, website_info in DOMAINS.iteritems():
        c = Crawler(website_name, website_info, 500, use_heuristic=use_heuristic)
        crawlers.append(c)
        c.start()

    for c in crawlers:
        c.join()

    export_all_crawled_pages(filename)
