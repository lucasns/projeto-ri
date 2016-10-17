from classifier.classifier import Classifier
from crawler.crawler import Crawler
from crawler.config import *
import cPickle as pickle
import csv
import os

def export_all_crawled_pages(filename):
    path = FILES_PATH

    results = {}

    for website_name in DOMAINS.keys():
        print(website_name)

        folder_path = os.path.join(path, website_name)

        if not os.path.exists(folder_path):
            continue

        results[website_name] = []

        for page in os.listdir(folder_path):
            f_name = os.path.join(folder_path, page)
            with open(f_name, 'r') as pagefile:
                results[website_name].append(pagefile.read())
            os.remove(f_name)

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

def harvest_ratio(pages, classifier):
    total = 0
    relevant = 0

    for domain in pages.keys():
        total += len(pages[domain])
        for p in pages[domain]:
            if classifier.classify(p):
                relevant += 1

    hr =  float(relevant) / total

    return hr

def save_csv(filename, rows):
    filename = os.path.join(DIR_PATH, filename+'.csv')
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def run():
    crawl(True, 'using-heuristic-pages.pickle')
    crawl(False, 'bfs-pages.pickle')

    classifier = Classifier()

    pages = import_crawled_pages('using-heuristic-pages.pickle')
    heuristic_hr = harvest_ratio(pages, classifier)

    pages = import_crawled_pages('bfs-pages.pickle')
    bfs_hr = harvest_ratio(pages, classifier)

    del pages

    rows = [['HR Heuristic', 'HR BFS'], [heuristic_hr, bfs_hr]]
    save_csv('harvest_ratio_results', rows)

if __name__ == '__main__':
    run()
