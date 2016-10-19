from bs4 import BeautifulSoup
import re


def _info_type(node):
    if node.name is not None:
        for child in node.children:
            if child.name is not None and child.string is not None:
                return 'Current'

    if node.name is not None:
        node = node.find_next()
        for child in node.children:
            if child.name is not None:
                return 'Next'

    return 'Sibling'


def extract_title(html):
    soup = BeautifulSoup(html, "lxml")
    
    title = soup.find(text=re.compile(r'[a-z0-9&]+[a-z0-9& ]*\([0-9]{4}\)'))
    if title is not None:
        title = title.string.split("(")[0]

    else:
        title = soup.find("h1")

        if title is not None:
            title = title.get_text(strip=True).split("(")[0]
    
    return title


def extract_synopsis(html):
    soup = BeautifulSoup(html, "lxml")
    synopsis = soup.find(text=re.compile(r'Synops'))
    if synopsis is not None:
        synopsis = synopsis.find_next().get_text(strip=True).replace("\n", " ")

      
    return synopsis


def extract_rating(html):
    soup = BeautifulSoup(html, "lxml")
    rating = soup.find(text=re.compile(r'MPAA.*[:|-]'))
    #print rating
    if rating is None:
        rating = soup.find(text=re.compile(r'^Rating.*[:|-]'))

    if rating is not None:
        rating = rating.find_next().string

    return rating


def extract_genre(html):
    soup = BeautifulSoup(html, "lxml")
    genre = soup.find(text=re.compile(r'Genre.*[:|-]'))
    
    if genre is not None:
        if genre.name is None:
            genre = genre.parent

        position = _info_type(genre)
       
        if position == 'Current':
            genre = [x.string.strip() for x in genre.findChildren() if x.string is not None]
        elif position == 'Next':
            genre = [x.string.strip() for x in genre.find_next().findChildren() if x.string is not None]
        elif position == 'Sibling':
            genre = [x.string.strip() for x in genre.find_next_siblings() if x.string is not None]


        genre = [x for x in genre if x != "," and x != "|"]

    return genre


def extract_director(html):
    soup = BeautifulSoup(html, "lxml")
    director = soup.find(text=re.compile(r'Direct.*[:|-]'))
    if director is not None:
        if director.name is None:
            director = director.parent

        position = _info_type(director)

        if position == 'Current':
            director = [x.text for x in director.findChildren() if x.string is not None]
        elif position == 'Next':
            director = [x.string.strip() for x in director.find_next().findChildren() if x.string is not None]
        elif position == 'Sibling':
            director = [x.string.strip() for x in director.find_next_siblings() if x.string is not None]
    
    return director


def extract_date(html):
    soup = BeautifulSoup(html, "lxml")
    date = soup.find(text=re.compile(r'[a-zA-Z]+ [0-9]{1,2},? [0-9]{4}.*'))

    if date is None:
        date = soup.find(text=re.compile(r'[0-9]{1,2} [a-zA-Z]+,? [0-9]{4}.*'))


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
    runtime = soup.find(text=re.compile(r'[0-9]+ ?min\.?'))


    if runtime is not None:
        runtime = runtime.strip()

    return runtime
