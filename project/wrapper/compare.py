import cPickle as pickle
import csv
import os


from wrapper import Wrapper, MovieInfo, extract_all

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def read_file():
    path = os.path.dirname(os.path.realpath(__file__))

    specresults = []
    genresults = []
    
    with open(os.path.join(path, "specific.pickle"), 'rb') as fspec, open(os.path.join(path, "generic.pickle"), 'rb') as fgen:
        count = 0;
        for x in xrange(1000):
            try:
                try:
                    specresults.append(pickle.load(fspec))

                    genresults.append(pickle.load(fgen))
                    count += 1
                    print count

                except Exception, e:
                    print e.message
                    break

            except EOFError:
                break

    return specresults, genresults


def evaluate(x, y):
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


def calculate(eval_list):
    tp = eval_list.count('TP')
    tn = eval_list.count('TN')
    fp = eval_list.count('FP')
    fn = eval_list.count('FN')

    precision = 0
    recall = 0
    accuracy = 0

    if tp + fp > 0:
        precision = float(tp) / (tp + fp)
          
    if tp + fn > 0:
         recall = float(tp) / (tp + fn)

    if tp + tn + fp + fn > 0:
        accuracy = float(tn + tp) / (tp + tn + fp + fn)

    return {'TP' : tp, 'FP' : fp, 'FN' : fn, 'TN': tn, 'precision' : precision, 'recall' : recall, 'accuracy' : accuracy}



def compare(specresults, genresults):
    results = {}

    results['title'] = [evaluate(specresults[i].title, genresults[i].title) for i in xrange(len(specresults))]
    results['synopsis'] = [evaluate(specresults[i].synopsis, genresults[i].synopsis) for i in xrange(len(specresults))]
    results['rating'] = [evaluate(specresults[i].rating, genresults[i].rating) for i in xrange(len(specresults))]
    results['genre'] = [evaluate(specresults[i].genre, genresults[i].genre) for i in xrange(len(specresults))]
    results['director'] = [evaluate(specresults[i].director, genresults[i].director) for i in xrange(len(specresults))]
    results['date'] = [evaluate(specresults[i].date, genresults[i].date) for i in xrange(len(specresults))]
    results['box_office'] = [evaluate(specresults[i].box_office, genresults[i].box_office) for i in xrange(len(specresults))]
    results['runtime'] = [evaluate(specresults[i].runtime, genresults[i].runtime) for i in xrange(len(specresults))]

    results_attributes = {}

    for key, value in results.iteritems():
        results_attributes[key] = calculate(value)


    mean_attributes = {'TP' : 0, 'FP' : 0, 'FN' : 0, 'TN': 0, 'precision' : 0, 'recall' : 0, 'accuracy' : 0}

    for key, value in results_attributes.iteritems():
        mean_attributes['TP'] += value['TP']
        mean_attributes['FP'] += value['FP']
        mean_attributes['FN'] += value['FN']
        mean_attributes['TN'] += value['TN']
        mean_attributes['precision'] += value['precision']
        mean_attributes['recall'] += value['recall']
        mean_attributes['accuracy'] += value['accuracy']


    for key, value in mean_attributes.iteritems():
        mean_attributes[key] = float(value)/8

    print mean_attributes

    results_movies = []
    for j in xrange(len(specresults)):
        results_movies.append(calculate([evaluate(specresults[j].get_info()[i], genresults[j].get_info()[i]) for i in xrange(1,9)]))

    mean_movie = {'TP' : 0, 'FP' : 0, 'FN' : 0, 'TN': 0, 'precision' : 0, 'recall' : 0, 'accuracy' : 0}

    for r in results_movies:
        mean_movie['TP'] += r['TP']
        mean_movie['FP'] += r['FP']
        mean_movie['FN'] += r['FN']
        mean_movie['TN'] += r['TN']
        mean_movie['precision'] += r['precision']
        mean_movie['recall'] += r['recall']
        mean_movie['accuracy'] += r['accuracy']

    for key, value in mean_movie.iteritems():
        mean_movie[key] = float(value)/len(results_movies)

    print mean_movie

    return results_attributes, mean_attributes, mean_movie
 

def save_csv(file, results, title, mode='wb'):
    filename = os.path.join(FILE_PATH, file + ".csv")

    rows = [[title], ["", "Possui Atributo", "Nao Possui Atributo"]]
    rows.append(["Retornou Atributo", results['TP'], results['FP']])
    rows.append(["Nao Retornou Atributo", results['FN'], results['TN']])
    rows.append([])
    rows.append(["Precision", results['precision']])
    rows.append(["Recall", results['recall']])
    rows.append(["Accuracy", results['accuracy']])
    rows.append([])
    rows.append([])

    with open(filename, mode) as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def run():
    filename = os.path.join(FILE_PATH, 'crawled_pages.pickle')

    with open(filename, 'rb') as f:
        results = pickle.load(f)

    extract_all(results)

    specresults, genresults = read_file()
    results_attributes, mean_attributes, mean_movie = compare(specresults, genresults)

    save_csv("results", mean_attributes, "Media", 'wb')
    
    for key, value in results_attributes.iteritems():
        save_csv("results", value, key, 'ab')

    save_csv("results", mean_movie, "Media Filme", 'ab')


if __name__ == '__main__':
    run()



