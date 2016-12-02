import csv
import os
import cPickle as pickle
from time import time

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

import classifier.tools as tools
from classifier.classifier import Classifier
from crawler.crawler import crawl_domain
from crawler.config import DOMAINS
from engine.index import IndexWriter, IndexReader
from wrapper.wrapper import Wrapper, MovieInfo
import consts
from utils import read_file, read_file_multiple, save_csv
from data import extract_all_info


#Crawler
def harvest_ratio(in_path, out_path, classifier):
    relevants = {}
    num_pages = {}

    for site in DOMAINS.iterkeys():
        relevants[site] = 0
        num_pages[site] = 0

    count = 0
    for site, html in read_file_multiple(in_path):
        count += 1
        print count
        num_pages[site] += 1
        if classifier.classify(html):
            relevants[site] += 1

    rows = [['Domain', '# Relevant pages', '# Downloaded pages', '# Harvest Ratio']]

    total_pages = 0
    total_relevants = 0

    
    for site in DOMAINS.iterkeys():
        total_pages += num_pages[site]
        total_relevants += relevants[site]
        domain_hr = float(relevants[site]) / num_pages[site]
        rows.append([site, relevants[site], num_pages[site], domain_hr])

    hr = float(total_relevants) / total_pages
    rows.append(['Total', total_relevants, total_pages, hr])

    save_csv(out_path, rows)


def compare_crawler():
    heuristic_file = os.path.join(consts.DATA_DIR, 'using-heuristic-pages.pickle')
    bsf_file = os.path.join(consts.DATA_DIR, 'bfs-pages.pickle')
    hr_bfs = os.path.join(consts.RESULTS_DIR, 'bfs_harvest_ratio_results.csv')
    hr_heuristic = os.path.join(consts.RESULTS_DIR, 'heuristic_harvest_ratio_results.csv')

    if not os.path.exists(heuristic_file):
        crawl(True, heuristic_file)

    if not os.path.exists(bfs_file):
        crawl(True, bsf_file)

    classifier = Classifier()

    harvest_ratio(heuristic_file, hr_heuristic, classifier)
    harvest_ratio(bsf_file, hr_bfs, classifier)


#Classifier
def list_scores(scores):
    res = [scores['accuracy'], scores['precision'], scores['recall'], scores['f1']]
    return res


def try_svm(features_train, features_test, labels_train, labels_test):
    C = [1, 10, 20, 100, 1000, 10000]
    kernels = ['rbf', 'linear', 'poly', 'sigmoid']

    rows = []

    for c in C:
        for kernel in kernels:
            alg_name = "SVM (C=%d, kernel=%s)" % (c, kernel)

            t0 = time()
            clf = SVC(C=c, kernel=kernel)
            clf.fit(features_train, labels_train)
            training_time = "%fs" % round(time() - t0, 3)

            scores = tools.evaluate(labels_test, clf.predict(features_test))

            rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_random_forest(features_train, features_test, labels_train, labels_test):
    N = [10, 20, 100, 200, 300, 10000]

    rows = []

    for n in N:
        alg_name = "Random Forest (N=%d)" % n

        t0 = time()
        clf = RandomForestClassifier(n_estimators = n)
        clf.fit(features_train, labels_train)
        training_time = "%fs" % round(time() - t0, 3)

        scores = tools.evaluate(labels_test, clf.predict(features_test))
        rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_regression(features_train, features_test, labels_train, labels_test):
    alg_name = "Linear Regression"

    t0 = time()
    clf = LinearRegression()
    clf.fit(features_train, labels_train)
    training_time = "%fs" % round(time() - t0, 3)

    rows = [[alg_name, training_time, clf.score(features_train, labels_train), "", "", ""]]

    return rows


def try_naive_bayes(features_train, features_test, labels_train, labels_test):
    alg_name = "Naive Bayes"

    t0 = time()
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    training_time = "%fs" % round(time() - t0, 3)

    scores = tools.evaluate(labels_test, clf.predict(features_test))

    rows = [[alg_name, training_time] + list_scores(scores)]

    return rows


def try_ada_boost(features_train, features_test, labels_train, labels_test):
    N = [1, 5, 10, 30, 40, 100, 1000]
    R = [0.1, 0.5, 0.7, 0.8, 0.9, 1]

    rows = []

    for n in N:
        for lr in R:
            alg_name = "AdaBoost (N=%d, learning_rate=%f)" % (n, lr)

            t0 = time()
            clf = AdaBoostClassifier(n_estimators=n, learning_rate=lr)
            clf.fit(features_train, labels_train)
            training_time = "%fs" % round(time() - t0, 3)

            scores = tools.evaluate(labels_test, clf.predict(features_test))

            rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def try_knn(features_train, features_test, labels_train, labels_test):
    N = [1, 5, 10, 20, 30, 35, 40]

    rows = []

    for n in N:
        alg_name = "k-NN (k=%d)" % n

        t0 = time()
        clf = KNeighborsClassifier(n_neighbors=n)
        clf.fit(features_train, labels_train)
        training_time = "%fs" % round(time() - t0, 3)

        scores = tools.evaluate(labels_test, clf.predict(features_test))
        rows.append([alg_name, training_time] + list_scores(scores))

    return rows


def compare_classifiers():
    db = tools.load_database()
    X, Y = tools.prepare_database(db)

    bag_of_words, bag_of_words_vectors = tools.create_bag_of_words(X)
    tfidf, tfidf_vectors = tools.create_TfIdf(X)

    print "Testing Bag of Words"

    file_path = os.path.join(consts.RESULTS_DIR, 'bag-of-words-results.csv')

    rows = [['Algorithm', 'Training Time', 'Accuracy', 'Precision', 'Recall', 'F1-Measure']]

    features_train, features_test, labels_train, labels_test = tools.split_dataset(bag_of_words_vectors, Y)

    rows += try_naive_bayes(features_train, features_test, labels_train, labels_test)
    rows += try_regression(features_train, features_test, labels_train, labels_test)
    rows += try_random_forest(features_train, features_test, labels_train, labels_test)
    rows += try_svm(features_train, features_test, labels_train, labels_test)
    rows += try_ada_boost(features_train, features_test, labels_train, labels_test)
    rows += try_knn(features_train, features_test, labels_train, labels_test)

    save_csv(file_path, rows)

    print "Testing TF-IDF"

    file_path = os.path.join(consts.RESULTS_DIR,  'tf-idf-resultss.csv')
    rows = [['Algorithm', 'Training Time', 'Accuracy', 'Precision', 'Recall', 'F1-Measure']]

    features_train, features_test, labels_train, labels_test = tools.split_dataset(tfidf_vectors, Y)

    rows += try_naive_bayes(features_train, features_test, labels_train, labels_test)
    rows += try_regression(features_train, features_test, labels_train, labels_test)
    rows += try_random_forest(features_train, features_test, labels_train, labels_test)
    rows += try_svm(features_train, features_test, labels_train, labels_test)
    rows += try_ada_boost(features_train, features_test, labels_train, labels_test)
    rows += try_knn(features_train, features_test, labels_train, labels_test)

    save_csv(file_path, rows)


#Wrapper
def _evaluate(x, y):
    if x is not None:
        if x == y:
            return 'TP'
        else:
            return 'FN'
    else:
        if y is None:
            return 'TN'
        else:
            return 'FP'


def _calculate(eval_list):
    tp = eval_list.count('TP')
    tn = eval_list.count('TN')
    fp = eval_list.count('FP')
    fn = eval_list.count('FN')

    precision = float(tp) / (tp + fp) if (tp + fp) > 0 else 0
    recall = float(tp) / (tp + fn) if (tp + fn) > 0 else 0
    accuracy = float(tn + tp) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0

    return {'TP' : tp, 'FP' : fp, 'FN' : fn, 'TN': tn, 'precision' : precision, 'recall' : recall, 'accuracy' : accuracy}


def extraction_score(specresults, genresults):
    results_attributes = {}

    results_attributes['Title'] = [_evaluate(specresults[i].title, genresults[i].title) for i in xrange(len(specresults))]
    results_attributes['Rating'] = [_evaluate(specresults[i].rating, genresults[i].rating) for i in xrange(len(specresults))]
    results_attributes['Genre'] = [_evaluate(specresults[i].genre, genresults[i].genre) for i in xrange(len(specresults))]
    results_attributes['Director'] = [_evaluate(specresults[i].director, genresults[i].director) for i in xrange(len(specresults))]
    results_attributes['Date'] = [_evaluate(specresults[i].date, genresults[i].date) for i in xrange(len(specresults))]
    results_attributes['Box Office'] = [_evaluate(specresults[i].boxoffice, genresults[i].boxoffice) for i in xrange(len(specresults))]
    results_attributes['Runtime'] = [_evaluate(specresults[i].runtime, genresults[i].runtime) for i in xrange(len(specresults))]

    results = {}

    for key, value in results_attributes.iteritems():
        results[key] = _calculate(value)

    mean_attributes = {'TP' : 0, 'FP' : 0, 'FN' : 0, 'TN': 0, 'precision' : 0, 'recall' : 0, 'accuracy' : 0}

    for key, value in results.iteritems():
        mean_attributes['TP'] += value['TP']
        mean_attributes['FP'] += value['FP']
        mean_attributes['FN'] += value['FN']
        mean_attributes['TN'] += value['TN']
        mean_attributes['precision'] += value['precision']
        mean_attributes['recall'] += value['recall']
        mean_attributes['accuracy'] += value['accuracy']

    for key, value in mean_attributes.iteritems():
        mean_attributes[key] = float(value)/8

    results['Media'] = mean_attributes

    return results


def compare_wrapper():
    specific_path = os.path.join(consts.DATA_DIR, "specific.pickle")
    generic_path = os.path.join(consts.DATA_DIR, "generic.pickle")

    if not os.path.exists(specific_path):
        extract_all_info(consts.CLASSIFIED_PATH, specific_path)

    if not os.path.exists(generic_path):
        extract_all_info(consts.CLASSIFIED_PATH, generic_path)

    specresults = read_file(specific_path)
    genresults = read_file(generic_path)
    
    results = extraction_score(specresults, genresults)

    order = ['Media', 'Title', 'Rating', 'Genre', 'Director', 'Date', 'Box Office', 'Runtime']

    rows = [["Atributo", "", ""], ["", "", ""]]

    for label in order:
        rows.append([label, "", ""])
        rows.append(["", "Possui Atributo", "Nao Possui Atributo"])
        rows.append(["Retornou Atributo", results[label]['TP'], results[label]['FP']])
        rows.append(["Nao Retornou Atributo", results[label]['FN'], results[label]['TN']])
        rows.append(["", "", ""])
        rows.append(["Precision", results[label]['precision'], ""])
        rows.append(["Recall", results[label]['recall'], ""])
        rows.append(["Accuracy", results[label]['accuracy'], ""])
        rows.append(["", "", ""])
        rows.append(["", "", ""])

    save_csv(os.path.join(consts.RESULTS_DIR, "wrapper_results.csv"), rows)


def compare_index():
    documents = read_file(consts.DOCUMENTS_PATH)
    tmp_index = os.path.join(consts.DATA_DIR, 'tmp_index.bin')

    rows = [["Data", "Size (KB)"]]

    statinfo = os.stat(consts.DOCUMENTS_PATH)
    size = int(statinfo.st_size/1024)
    rows.append(["Documents Dict", size])

    writer = IndexWriter(False)
    writer.write_index(documents, tmp_index)

    statinfo = os.stat(tmp_index)
    size = int(statinfo.st_size/1024)
    rows.append(["Index Uncompressed", size])

    writer = IndexWriter(True)
    writer.write_index(documents, tmp_index)

    statinfo = os.stat(tmp_index)
    size = int(statinfo.st_size/1024)
    rows.append(["Index VB Encoded", size])
    save_csv(os.path.join(consts.RESULTS_DIR, "index_results.csv"), rows)


if __name__ == '__main__':
    if not os.path.exists(consts.RESULTS_DIR):
        os.makedirs(consts.RESULTS_DIR)

    if not os.path.exists(consts.DATA_DIR):
        os.makedirs(consts.DATA_DIR)

    compare_classifiers()
    compare_crawler()
    compare_wrapper()
    compare_index()
