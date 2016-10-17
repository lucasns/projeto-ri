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

def save_csv(filename, rows):
    filename = os.path.join(FILES_PATH, filename+'.csv')
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def harvest_ratio(pages, classifier, filename):
    total = 0
    relevant = 0

    rows = [['Domain', '# Relevant pages', '# Downloaded pages', '# Harvest Ratio']]

    for domain in pages.keys():
        num_pages = len(pages[domain])
        domain_relevant = 0

        for p in pages[domain]:
            if classifier.classify(p):
                domain_relevant += 1

        total += num_pages
        relevant += domain_relevant

        domain_hr = float(domain_relevant) / num_pages

        rows.append([domain, domain_relevant, num_pages, domain_hr])

    hr =  float(relevant) / total

    rows.append(['Total', relevant, total, hr])

    save_csv(filename, rows)

def run():
    crawl(True, 'using-heuristic-pages.pickle')
    crawl(False, 'bfs-pages.pickle')

    classifier = Classifier()

    pages = import_crawled_pages('using-heuristic-pages.pickle')
    harvest_ratio(pages, classifier, 'heuristic_harvest_ratio_results')

    pages = import_crawled_pages('bfs-pages.pickle')
    harvest_ratio(pages, classifier, 'bfs_harvest_ratio_results')

if __name__ == '__main__':
    run()
