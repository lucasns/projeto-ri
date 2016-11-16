import cPickle as pickle
import csv
import os
import sys

from wrapper import Wrapper, MovieInfo


FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def read_file_multiple(file):
    content = []
    
    with open(file, 'rb') as f:
        while True:
            try:
                content.append(pickle.load(f))
            except EOFError:
                break

    return content


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
 

def save_csv(file, rows):
    with open(file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def compare_wrapper():
    specresults = read_file_multiple(os.path.join(FILE_PATH, "specific.pickle"))
    genresults = read_file_multiple(os.path.join(FILE_PATH, "generic.pickle"))
    
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

    save_csv(os.path.join(FILE_PATH, "results/results.csv"), rows)


if __name__ == '__main__':
    compare_wrapper()
