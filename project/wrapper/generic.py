from bs4 import BeautifulSoup
import re


def extract_title(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h1")
    if title is not None:
        title = title.get_text(strip=True)
    
    return title


def extract_synopsis(html):
    soup = BeautifulSoup(html, "lxml")
    synopsis = soup.find(text=re.compile(r'Synops'))
    if synopsis is not None:
        synopsis = synopsis.find_next().get_text(strip=True).replace("\n", " ")
      
    return synopsis


def extract_rating(html):
    soup = BeautifulSoup(html, "lxml")
    rating = soup.find(text=re.compile(r'^Rating.*[:|-]'))
    if rating is not None:
        rating = rating.find_next().string

    return rating


def extract_genre(html):
    soup = BeautifulSoup(html, "lxml")
    genre = soup.find(text=re.compile(r'Genre.*[:|-]'))
    if genre is not None:
        genre = genre.parent
        genre = [x.string for x in genre.find_next_siblings()]
    
    return genre


def extract_director(html):
    soup = BeautifulSoup(html, "lxml")
    director = soup.find(text=re.compile(r'Direct.*[:|-]'))
    if director is not None:
        director = director.parent
        director = [x.text.strip() for x in director.find_next_siblings()]
    
    return director


def extract_date(html):
    soup = BeautifulSoup(html, "lxml")
    date = soup.find(text=re.compile(r'[a-z]+ [0-9]{2},? [0-9]{4}'))
    if date is not None:
        date = date.strip()
    
    return date


def extract_boxoffice(html):
    soup = BeautifulSoup(html, "lxml")
    box_office = soup.find(text=re.compile(r'\$[0-9]+[,|.]+[0-9]+[,|.]+[0-9]+'))
    if box_office is not None:
        box_office = box_office.strip()

    return box_office


def extract_runtime(html):
    soup = BeautifulSoup(html, "lxml")
    runtime = soup.find(text=re.compile(r'[0-9]+ ?min.?'))
    if runtime is not None:
        runtime = runtime.strip()

    return runtime


