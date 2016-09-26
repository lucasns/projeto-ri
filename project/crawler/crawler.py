import urllib2
import threading
import requests
import time
import re
import os
import cPickle as pickle
from urlparse import urljoin
from bs4 import BeautifulSoup


DOMAINS = {
            'rottentomatoes':   {'seed': 'https://www.rottentomatoes.com/',
                                 'robots_txt': ['license/export/', 'search', 'user', 'click',
                                                'logout', 'trailer', 'login', 'ajax'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://www.rottentomatoes.com/m/.*/$'
                                },

            'imdb':             {'seed': 'http://www.imdb.com/',
                                 'robots_txt': ['tvschedule', 'ActorSearch', 'ActressSearch', 'AddRecommendation',
                                                'ads/', 'AlternateVersions', 'AName', 'Awards', 'BAgent', 'Ballot/',
                                                'BornInYear', 'BornWhere', 'BPublicity', 'BQuotes', 'BTrivia',
                                                'BusinessThisDay', 'BWorks', 'careers', 'help/show_leaf?careeratimdb',
                                                'CommentsAuthor', 'CommentsEnter', 'CommentsIndex', 'Companies',
                                                'CrazyCredits', 'Credits', 'DiedInYear', 'DiedWhere', 'DVD', 'ExciteTitle',
                                                'Find', 'FName', 'GName', 'Guests', 'harvest_me', 'HelpPage', 'Icons/',
                                                'JointVentures', 'Laserdisc', 'List', 'Literature', 'Locations',
                                                'LocationTree', 'Lookup', 'M/', 'Maltin', 'MarriedInYear', 'MetaSearch',
                                                'Mlinks', 'More', 'Movies', 'Movies/', 'MyMovies', 'mymovies/',
                                                'name_pick_n_mix', 'Nsearch', 'NUrls', 'OnThisDay', 'Ontv', 'OnTV',
                                                'Overlap', 'Pawards', 'pick_n_mix', 'PName', 'Posters', 'prepare_data',
                                                'Psales', 'Quiz', 'r/', 'ra/', 'Ratings', 'rd/', 'Recommendations',
                                                'register', 'ReleaseDates', 'ReleasedInYear', 'Reviews', 'rg/', 'ri/',
                                                'RName', 'Sales', 'SearchAwards', 'SearchBios', 'SearchBusiness',
                                                'SearchCrazy', 'SearchDVD', 'SearchGoofs', 'SearchLaserdisc',
                                                'SearchLiterature', 'SearchPlots', 'SearchPlotWriters', 'SearchQuotes',
                                                'SearchRatios', 'SearchSongs', 'SearchTaglines', 'SearchTechnical',
                                                'SearchTrivia', 'SearchVersions', 'ShowAll', 'Showing', 'SName',
                                                'Soundtracks', 'Taglines', 'Tawards', 'Technical', 'tiger_redirect',
                                                'Title/ASIN', 'TitleBrowse', 'Trailers', 'Tsearch', 'TUrls', 'VName',
                                                'Vote', 'WorkedWith', 'updates', 'board', 'boards'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.imdb.com/title/.*/'
                                },

            'metacritic':       {'seed': 'http://www.metacritic.com/',
                                 'robots_txt': ['search', 'signup', 'login', 'user', 'jl/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.metacritic.com/movie/[^/\?]*$'
                                },

            'movies':           {'seed': 'http://www.movies.com/',
                                 'robots_txt': ['undefined', 'Bin/', 'backlot/', 'controls/', 'reviews/controls/',
                                                'exclusives/controls/','search', 'narrow-your-search-results',
                                                'search-results', 'search-result', 'page-not-found'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.movies.com/[^/\?]*/m[0-9]*$'
                                },

            'allmovie':         {'seed': 'http://www.allmovie.com/',
                                 'robots_txt': ['admin', 'user/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.allmovie.com/movie/[^/\?]*$'
                                },

            'flixster':         {'seed': 'https://www.flixster.com/',
                                 'robots_txt': ['actor/random', 'admin', 'address-book', 'api', 'bebo', 'captcha',
                                                 'converse.do', 'DoNotSend.jsp', 'facebook', 'friendsAction.do',
                                                 'friends.do', 'global-scripts', 'hi5', 'igoogle', 'invite',
                                                 'inviteDisplay.do', 'mctResults.do', 'metrics', 'mmessage',
                                                 'movie-facts', 'myspace', 'news/saved-stories',
                                                 'news/submitted-stories', 'page-scripts', 'people',
                                                 'people.do', 'rate-movies', 'recommendations', 'static/scripts',
                                                 'support', 'userAuth.do', 'ad.do', 'sponsors', 'misc',
                                                 'email-content', 'static/ads', 'user/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://www.flixster.com/movie/[^/\?]*$'
                                },

            'tribute':          {'seed': 'http://www.tribute.ca/',
                                 'robots_txt': ['demo/', 'tvlistings/', 'ads/', 'doubleclick/', 'flash/', 'feeds/',
                                                'controls/', 'aspnet_client/', 'pages/', 'app_data/', 'css/',
                                                'lib/', 'config/', 'aspnet_client/', 'rma/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.tribute.ca/movies/[^/\?]*/[0-9]*/$'
                                },

            'boxofficemojo':    {'seed': 'http://www.boxofficemojo.com/',
                                 'robots_txt': ['movies/default.movies.htm', 'showtimes/buy.php', 'forums/',
                                 'derbygame/', 'grades/', 'moviehangman/', 'users/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.boxofficemojo.com/movies/\?id=.*'
                                },

            'mubi':             {'seed': 'https://mubi.com/',
                                 'robots_txt': ['login'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://mubi.com/films/*[^/\?]*$'
                                },

            'yify':             {'seed': 'http://yify.info/',
                                 'robots_txt': ['engine/go.php', 'engine/download.php', 'user/', 'newposts/',
                                                'statistics.html'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://yify.info/.*'
                                }
        }


class Crawler(threading.Thread):
    def __init__(self, website_name, website_info, use_heuristic=False):
        threading.Thread.__init__(self)
        self.website_name = website_name
        self.website_info = website_info
        self.use_heuristic = use_heuristic
        self.crawled_websites = []
        self.frontier = [website_info['seed']]
        self.visited = [website_info['seed']]
        self.disallowed_links = [urljoin(website_info['seed'], link)
                                 for link in website_info['robots_txt']]


    def match_heuristic(self, url):
        return re.match(self.website_info['movies_pattern'], url)
    

    def is_html(self, url):
        r = requests.head(url)
        return "text/html" in r.headers["content-type"]
       
     
    def get_html(self, url):
        user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        page = urllib2.Request(url, headers=user_agent)
        page = urllib2.urlopen(page)
        html = page.read()
        
        return html

    
    def get_urls(self, html):
        soup = BeautifulSoup(html, "lxml")
        anchor_tags = soup.find_all('a', href=True)
        
        urls = [urljoin(self.website_info['seed'], link['href']) for link in anchor_tags]

        urls = [u for u in urls if (self.website_info['seed'] in u and
                                    u not in self.disallowed_links)]
        
        return urls


    def run(self):
        max_pages = 500

        while len(self.frontier) > 0 and len(self.crawled_websites) < max_pages:
            index = 0
            if self.use_heuristic:
                for i, url in enumerate(self.frontier):
                    if self.match_heuristic(url):
                        index = i
                        break
            
            curr_url = self.frontier.pop(index)
            time.sleep(self.website_info['sleep_time'])

            try:
                if not self.is_html(curr_url):
                    continue
                
                html = self.get_html(curr_url)
                
                self.crawled_websites.append(html)
                print(curr_url)

                for url in self.get_urls(html):
                    if url not in self.visited:
                        self.frontier.append(url)
                        self.visited.append(url)

            except Exception,e:
                print("\nERROR WITH URL: " + curr_url)
                print("ERROR MESSAGE: " + str(e.message) + '\n')


    def save_crawled_pages(self, results):
        results[self.website_name] = self.crawled_websites


def get_files_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files_path = os.path.join(dir_path, 'files')

    if not os.path.exists(files_path):
        os.makedirs(files_path)

    return files_path


def export_all_crawled_pages():
    files_path = get_files_path()

    with open(os.path.join(files_path, 'results.pickle'), 'rb') as f:
        results = pickle.load(f)

    for website_name, crawled_pages in results.items():
        folder_path = os.path.join(files_path, website_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for idx, html in enumerate(crawled_pages, start=1):
            file_complete_name = os.path.join(folder_path, website_name+'_'+str(idx)+".html")

            with open(file_complete_name, "w") as f:
                f.write(html)
           

def crawl():
    crawlers = []
    for website_name, website_info in DOMAINS.iteritems():
        c = Crawler(website_name, website_info, True)
        crawlers.append(c)
        c.start()

    results = {}

    for c in crawlers:
        c.join()
        c.save_crawled_pages(results)

    with open(os.path.join(get_files_path(), 'results.pickle'), 'wb') as f:
        pickle.dump(results, f)


if __name__ == '__main__':
    crawl()
    export_all_crawled_pages()
