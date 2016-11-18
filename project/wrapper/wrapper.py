import collections
import cPickle as pickle
import os
import sys

from bs4 import BeautifulSoup

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


def read_file_multiple(file_path):
    with open(file_path, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def extract_info_file(in_path, out_path, extract_type='specific'):
    wrapper = Wrapper()

    if extract_type == 'generic':
        extract_funtion = wrapper.extract_generic
    else:
        extract_funtion = wrapper.extract_specific
    
    with open(out_path, 'wb') as f:
        info_list = []
        for site, html in read_file_multiple(in_path):
            info = extract_funtion(html, site)
            info_list.append(info)
        
        pickle.dump(info_list, f, pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))

    extract_info_file(os.path.join(path, "../../data/classified_pages.pickle"), os.path.join(path, "../../data/specific.pickle"))
    extract_info_file(os.path.join(path, "../../data/classified_pages.pickle"), os.path.join(path, "../../data/generic.pickle"), 'generic')
 