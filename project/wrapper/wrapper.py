from specific import *
from bs4 import BeautifulSoup


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

        if list:
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
                          "Genre: " + str(None) if self.genre is None else ", ".join(self.genre),
                          "Director: " + str(None) if self.director is None else ", ".join(self.director),
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


    def extract_specific(self, site, html):
        soup = BeautifulSoup(html, "lxml")
        info = self.specfunc[site](soup)
        movie_info = MovieInfo(info)
        return movie_info

