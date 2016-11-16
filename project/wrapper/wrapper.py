from bs4 import BeautifulSoup
import collections
import cPickle as pickle
import os
import sys

import generic
import specific


MovieInfo = collections.namedtuple('MovieInfo', 'site, url, title, rating, genre, director, date, boxoffice, runtime')


class Wrapper(object):
    def __init__(self):
        self._funcs = {'rottentomatoes': specific.extract_rottentomatoes,
                        'imdb': specific.extract_imdb,
                        'metacritic': specific.extract_metacritic,
                        'movies': specific.extract_movies,
                        'allmovie': specific.extract_allmovie,
                        'flixster': specific.extract_flixster,
                        'tribute': specific.extract_tribute,
                        'boxofficemojo': specific.extract_boxofficemojo,
                        'mubi': specific.extract_mubi,
                        'yify': specific.extract_yify,
                        'generic': generic.extract_info}


    def _format_info(self, info):
        r = []
        for e in info:
            if type(e) is list:
                e = [i.encode('utf-8') for i in e]
            elif e is not None:
                e = e.encode('utf-8')

            r.append(e)

        return tuple(r)


    def extract_specific(self, html, site, url = None):
        info = (site, url) + self._funcs[site](html)
        movie_info = MovieInfo._make(self._format_info(info))
        return movie_info


    def extract_generic(self, html, site, url = None):
        info = (site, url) + self._funcs['generic'](html)
        movie_info = MovieInfo._make(self._format_info(info))
        return movie_info


def read_file(file):
    content = None
    with open(file) as f:
        content = pickle.load(f)

    return content


def extract_all(results):
    path = os.path.dirname(os.path.realpath(__file__))

    w = Wrapper()
        
    count = 0
    with open(os.path.join(path, "../../data/specific.pickle"), 'wb') as fspec, open(os.path.join(path, "../../data/generic.pickle"), 'wb') as fgen:
        for site in results.iterkeys():
            for i in xrange(len(results[site])):
                html = results[site][i]
                count += 1
                print site + " " + str(count)
            
                spec = w.extract_specific(html, site)
                gen = w.extract_generic(html, site)
                
                pickle.dump(spec, fspec, pickle.HIGHEST_PROTOCOL)
                pickle.dump(gen, fgen, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    results = {}

    with open(os.path.join(path, "classified_pages.pickle"), 'rb') as f:
        results = pickle.load(f)

    extract_all(results)
