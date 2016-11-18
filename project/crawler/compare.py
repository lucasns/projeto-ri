import csv
import os
import sys

from tools import import_crawled_pages, crawl


sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from classifier.classifier import Classifier

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
