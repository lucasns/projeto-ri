import re
from bs4 import BeautifulSoup


def extract_rottentomatoes(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    #Site
    site = "rottentomatoes"

    #Title
    title = soup.find(id="movie-title")
    if title is not None:
        title = title.contents[0].strip()

    #Synopsis
    synopsis = soup.find("div", id="movieSynopsis")
    if synopsis is not None:
        synopsis = synopsis.string.strip()

    #Rating
    rating = soup.find(text="Rating:")
    if rating is not None:
        rating = rating.find_next().string

    #Genre
    genre = soup.find(text="Genre:")
    if genre is not None:
        genre = genre.find_next()
        genre = [i.string for i in genre.find_all("span")]

    #Director
    director = soup.find(text="Directed By:")
    if director is not None:
        director = director.find_next()
        director = [i.string for i in director.find_all("span")]

    #Writer
    writer = soup.find(text="Written By:")
    if writer is not None:
        writer = writer.find_next()
        writer = [i.string for i in writer.find_all("span")]

    #Date
    date = soup.find(text="In Theaters:")
    if date is not None:
        date = date.find_next().get_text(" ", strip=True).title()

    #Box Office
    box_office = soup.find(text="Box Office:")
    if box_office is not None:
        box_office = box_office.find_next().string

    #Runtime
    runtime = soup.find(text="Runtime:")
    if runtime is not None:
        runtime = runtime.find_next().get_text(strip=True)

    #Studio
    studio = soup.find(text="Studio:")
    if studio is not None:
        studio = studio.find_next().get_text(strip=True)
    
    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_imdb(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    #Site
    site = "imdb"
    
    #Title
    title = soup.find("div", class_="originalTitle")
    if title is not None:
        title = title.get_text()
    
    #Rating
    rating = soup.find(itemprop="contentRating")
    if rating is not None:
        rating = rating.attrs['content']

    #Synopsis
    synopsis = soup.find(class_="summary_text")
    if synopsis is not None:
        synopsis = synopsis.get_text(strip=True).replace("\n", " ")
    
    #Director
    director = soup.find_all(itemprop="director")
    director = [i.get_text(strip=True) for i in director] if director else None
    
    #Genres
    genre = soup.find("div", itemprop="genre")
    if genre is not None:
        genre = [i.get_text() for i in genre.find_all("a")]

    #Details Div
    info = soup.find("div", id="titleDetails")
    
    #Date
    date = soup.find(text="Release Date:")
    if date is not None:
        date = date.next_element.strip()
  
    #Box Office
    box_office = soup.find(text="Gross:")
    if box_office is not None:
       box_office = box_office.next_element.strip()

    #Runtime
    runtime = soup.find(itemprop="duration")
    if runtime is not None:
        runtime = runtime.get_text(strip=True)
    
    #Writer
    writer = soup.find("h4", text=re.compile(r"Writer"))
    if writer is not None:
        writer = [i.get_text(strip=True) for i in writer.parent.find_all(itemprop="creator")]

    #Stars
    stars = soup.find_all(itemprop="actors")
    stars = [i.get_text(strip=True) for i in stars] if stars else None

    #Producer
    producer = soup.find("h4", text="Production Co:")
    if producer is not None:
        producer =  [i.get_text().strip() for i in producer.parent.find_all(itemprop="creator")]

    #Country
    country = soup.find("h4", text="Country:")
    if country is not None:
        country =  [i.get_text().strip() for i in country.parent.find_all("a")]

    #Language
    language = soup.find("h4", text="Language:")
    if language is not None:
        language =  [i.get_text().strip() for i in language.parent.find_all("a")]
    

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_metacritic(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    info = soup.find(class_="summary_wrap")

    #Site
    site = "metacritic"

    #Title
    title = soup.find(class_="product_title")
    if title is not None:
        title = title.get_text(strip=True)

    #Synopsis
    synopsis = soup.find(itemprop="description")
    if synopsis is not None:
        synopsis = synopsis.string.strip().replace("\n", " ")

    #Rating
    rating = soup.find(class_="summary_detail product_rating")
    if rating is not None:
        rating = rating.find(itemprop="contentRating").string

    #Genre
    genre = soup.find(class_="summary_detail product_genre")
    if genre is not None:
        genre = [i.string.strip() for i in genre.find_all(itemprop="genre")]

    #Director
    director = soup.find(class_="summary_detail developer")
    if director is not None:
        director = [i.string.strip() for i in director.find_all(itemprop="name")]
        
    #Date
    date = soup.find(class_="summary_detail release_data")
    if date is not None:
        date = date.find(class_="data").string.strip()

    #Runtime
    runtime = soup.find(itemprop="duration")
    if runtime is not None:
        runtime = runtime.find_next().string

    #Box Office

    #Studio
    studio = soup.find(class_="summary_detail publisher")
    if studio is not None:
        studio = studio.find(itemprop="name").string.strip()

    #Starring
    starring = soup.find(class_="summary_detail product_credits")
    if starring is not None:
        starring =  [i.string.strip() for i in starring.find_all(itemprop="name")]

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_movies(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    #Site
    site = "movies"

    #Title
    title = soup.find("h1")
    if title is not None:
        title = title.string

    #Synopsis
    synopsis = soup.find(class_="segment")
    if synopsis is not None:
        synopsis = synopsis.p.text.strip().replace("\n", " ")
        synopsis = synopsis if "more" not in synopsis else synopsis[:len(synopsis)-4]


    movie_specs = soup.find(id="movieSpecs")
    if movie_specs is not None:
        movie_specs = movie_specs.find_all("li")

        #Rating
        rating = movie_specs[1].find("img").attrs['title']
        if rating is not None:
            rating = rating[6:].upper()

        #Genre
        genre = movie_specs[3].text.split(": ")[1]
        if genre is not None:
            genre = genre.split(", ")

        #Director
        director = [i.string for i in movie_specs[4].find_all("a")]

        #Date
        date = movie_specs[0].text.split(": ")[1].strip()

        #Box Office

        #Runtime
        runtime = movie_specs[2].text.split(": ")[1].strip()

        #Cast
        cast = [i.string for i in movie_specs[5].find_all("a") if i.string not in "Full cast + crew"]

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_allmovie(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    details = soup.find(class_="details")

    #Site
    site = "allmovie"

    #Title
    title = soup.find(class_="movie-title")
    if title is not None:
        title = title.get_text(strip=True).split("(")[0]
    
    #Synopsis
    synopsis = soup.find(class_="text")
    if synopsis is not None:
        synopsis = synopsis.get_text(strip=True).replace("\n", " ")
    
    #Rating
    rating = soup.find(text="MPAA Rating")
    if rating is not None:
       rating = rating.find_next().string

    #Genres
    genre = soup.find(class_="header-movie-genres")
    if genre is not None:
        genre = [i.get_text() for i in genre.find_all("a")]

    #Director
    director = soup.find(class_="movie-director")
    if director is not None:
        director = [i.get_text() for i in director.find_all("a")]
  
    #Release Date
    date = soup.find(text=re.compile(r'Release Date'))
    if date is not None:
        date = date.parent.span.string

    #Runtime
    runtime = soup.find(text=re.compile(r'Run Time'))
    if runtime is not None:
        runtime = runtime.parent.span.string

    #Studio
    studio = soup.find(text="Released By")
    if studio is not None:
        studio = studio.find_next().string

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_flixster(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    attributes = soup.find(class_="attributes")

    #Site
    site = "flixster"

    #Title
    title = soup.find(class_="title")
    if title is not None:
        title = title.string
    
    #Synopsis
    synopsis = soup.find(class_="synopsis")
    if synopsis is not None:
        synopsis = synopsis.get_text(strip=True).replace("\n", " ")

    #Rating
    rating = soup.find(itemprop="contentRating")
    if rating is not None:
        rating = rating.string

    #Genre
    genre = soup.find_all(itemprop="genre")
    if genre:
        genre = [i.string for i in genre] if genre else None
    else:
        genre = None
    
    #Director
    director = soup.find_all(itemprop="name")
    if director:
        director = [i.string for i in director]
    else:
        director = None

    #Date
    date = soup.find(class_="release-date")
    if date is not None:
        date = date.find(class_="value").string.strip()

    #Box Office

    #Runtime
    runtime = soup.find(itemprop="duration")
    if runtime is not None:
        runtime = runtime.string

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_tribute(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9
     
    #Site
    site = "tribute"

    #Title
    title = soup.find(class_="maintitle")
    if title is not None:
        title = title.get_text(strip=True)

    #Synopsis
    synopsis = soup.find("h2", text="Synopsis")
    if synopsis is not None:
        synopsis = synopsis.find_next().find_next().get_text()

    #Rating

    #Genre
    genre = soup.find(text="Genre:")
    if genre is not None:
        genre = genre.find_next()
        genre = [i.string for i in genre.find_all("a")]
    
    #Director
    director = soup.find(text="Director: ")

    if director is not None:
        director = director.find_next()
        director = director.get_text().split(", ")

    #Date
    date = soup.find(text="In theatres:")
    if date is not None:
        date = date.find_next().string
 
    #Box Office

    #Runtime
    runtime = soup.find(text="Running Time:")
    if runtime is not None:
        runtime = runtime.next_element.strip()
  
    #Studio
    studio = soup.find(text="Studio: ")
    if studio is not None:
        studio = studio.find_next().string

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def _boxofficemojo_get_list(aux):
    aux = aux.find_next("font")
    aux = map(lambda x: x.string, aux)
    aux = filter(lambda x: x != ' ', aux)

    list = []
    string = ""
    for i in range(len(aux)):
        if i == len(aux)-1:
            string += aux[i]
            list.append(string)
        elif aux[i] is None:
            list.append(string)
            string = ""
        else:
            string += aux[i]

    return list


def extract_boxofficemojo(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9
      
    #Site
    site = "boxofficemojo"

    #Title
    title = soup.find(style="padding-top: 5px;")
    if title is not None:
        title = title.find_next("td").find_next("td").font.get_text(strip=True)

    #Synopsis
    
    #Director
    director = soup.find(text=re.compile(r'Director'))
    if director is not None:
        director = _boxofficemojo_get_list(director)

    table = soup.find("table", width="95%")
    if table is not None:
        rows = table.find_all("tr")

        #Rating
        rating = rows[3].find_all("td")
        rating = rating[0].b.string

        #Genre
        genre = rows[2].find_all("td")
        genre = genre[0].b.string.split(", ")

        #Date
        date = rows[1].find_all("td")[1]
        date = date.find("a").string

        #Box Office
        box_office = rows[0].find("font", size="4")
        box_office = box_office.b.string

        #Runtime
        runtime = rows[2].find_all("td")[1].b.string

    #Writer
    writer = soup.find(text=re.compile(r'Writer'))
    if writer is not None:
        writer = _boxofficemojo_get_list(writer)

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_mubi(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    #Site
    site = "mubi"

    #Title
    title = soup.find(class_="film-show__titles__title condensed-header")
    if title is not None:
        title = title.string

    #Synopsis
    synopsis = soup.find("p", itemprop="description")
    if synopsis is not None:
        synopsis = synopsis.string.replace("\n", " ")

    #Rating

    #Genre
    genre = soup.find(class_="film-show__genres")
    if genre is not None:
        genre = genre.string.strip().split(", ")

    #Director
    director = soup.find(class_="film-show__directors")
    if director is not None:
        director = [i.string for i in director.find_all(itemprop="name")]

    #Date
    date = soup.find(class_="film-show__country-year")
    if date is not None:
        date = date.string.split(", ")[1]

    #Box Office

    #Runtime
    runtime = soup.find(itemprop="duration")
    if runtime is not None:
        runtime = runtime.string.strip()

    #Country
    country = soup.find(class_="film-show__country-year")
    if country is not None:
        country = country.string.split(", ")[0]

    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info


def extract_yify(html):
    soup = BeautifulSoup(html, "lxml")
    site, title, synopsis, rating, genre, director, date, box_office, runtime = [None] * 9

    #Site
    site = "yify"

    #Title
    title = soup.find(class_="post-title")
    if title is not None:
        title = title.get_text(strip=True).split(" (")[0]

    table = soup.find("ul", class_="table")
    if table is not None:
        rows = table.find_all("li")
   
        #Synopsis
        synopsis = rows[8].text[6:].replace("\n", " ")
    
        #Rating
        rating = rows[7].find("a").string

        #Genre
        genre = [i.string for i in rows[1].find_all("a")]

        #Director
        director = [i.string for i in rows[3].find_all("a")]

        #Date
        date = rows[0].find("a").string

        #Box Office

        #Cast
        cast = [i.string for i in rows[4].find_all("a")]

        #Country
        country = rows[5].find("a").string

        #Language
        language = rows[6].find("a").string

    #Runtime
    runtime = soup.find(text=re.compile(r'Runtime:'))
    if runtime is not None:
        runtime = runtime.split(": ")[1]
    
    full_info = site, title, synopsis, rating, genre, director, date, box_office, runtime
    return full_info
