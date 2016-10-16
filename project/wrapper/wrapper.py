from bs4 import BeautifulSoup
import cPickle as pickle
import os
import sys

from generic import *
from specific import *


class MovieInfo(object):
    def __init__(self, info=[]):
        self.site = None
        self.title = None
        self.synopsis = None
        self.rating = None
        self.genre = None
        self.director = None
        self.date = None
        self.box_office = None
        self.runtime = None

        if info:
            self.set_info(info)
        

    def get_info(self):
        return self.site, self.title, self.synopsis, self.rating, self.genre, self.director, self.date, self.box_office, self.runtime

    
    def set_info(self, info_list):
        self.site, self.title, self.synopsis, self.rating, self.genre, self.director, self.date, self.box_office, self.runtime = info_list


    def __repr__(self):
        return "\n".join(("Site: " + str(self.site),
                          "Title: " + str(self.title),
                          "Synopsis: " + str(self.synopsis),
                          "MPPA Rating: " + str(self.rating),
                          "Genre: " + (str(None) if self.genre is None else ", ".join(self.genre)),
                          "Director: " + (str(None) if self.director is None else ", ".join(self.director)),
                          "Release Date: " + str(self.date),
                          "Box Office: " + str(self.box_office),
                          "Runtime: " +  str(self.runtime)))


class Wrapper(object):
    def __init__(self):
        self.specfunc = {"rottentomatoes": extract_rottentomatoes,
                         "imdb": extract_imdb,
                         "metacritic": extract_metacritic,
                         "movies": extract_movies,
                         "allmovie": extract_allmovie,
                         "flixster": extract_flixster,
                         "tribute": extract_tribute,
                         "boxofficemojo": extract_boxofficemojo,
                         "mubi": extract_mubi,
                         "yify": extract_yify}


    def extract_specific(self, html, site):
        info = self.specfunc[site](html)
        movie_info = MovieInfo(info)
        return movie_info


    def extract_generic(self, html, site):
        title = extract_title(html)
        synopsis = extract_synopsis(html)
        rating = extract_rating(html)
        genre = extract_genre(html)
        director = extract_director(html)
        date = extract_date(html)
        box_office = extract_boxoffice(html)
        runtime = extract_runtime(html)

        info = site, title, synopsis, rating, genre, director, date, box_office, runtime

        movie_info = MovieInfo(info)
        return movie_info


def extract_all(results):
    path = os.path.dirname(os.path.realpath(__file__))
    sys.setrecursionlimit(10000)

    specresults = []
    genresults = []

    w = Wrapper()
        
    count = 0
    with open(os.path.join(path, "specific.pickle"), 'wb') as fspec, open(os.path.join(path, "generic.pickle"), 'wb') as fgen:
        for site in results.iterkeys():
            print site
            for i in xrange(100):
                html = results[site][i]
                count += 1
                print count
            
                spec = w.extract_specific(html, site)
                gen = w.extract_generic(html, site)
                pickle.dump(spec, fspec, pickle.HIGHEST_PROTOCOL)
                pickle.dump(gen, fgen, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    results = {}

    with open(os.path.join(path, "crawled_pages.pickle"), 'rb') as f:
        results = pickle.load(f)

    extract_all(results)
