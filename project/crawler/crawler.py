import urllib2
import threading
import requests
import time
import re
import os.path
import pickle
from urlparse import urljoin
from bs4 import BeautifulSoup


DOMAINS = { 
            'rottentomatoes':   {'seed': 'https://www.rottentomatoes.com/',
                                 'robots_txt': ['license/export/', 'search', 'user', 'click', 'logout', 'trailer', 'login', 'ajax'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://www.rottentomatoes.com/m/.*'
                                },
            'imdb':             {'seed': 'http://www.imdb.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.imdb.com/title/.*'
                                },
            'metacritic':       {'seed': 'http://www.metacritic.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.metacritic.com/movie/.*'
                                },
            'movies':           {'seed': 'http://www.movies.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.movies.com/.*/m.*'
                                },
            'allmovie':         {'seed': 'http://www.allmovie.com/',
                                 'robots_txt': ['admin', 'user/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.allmovie.com/movie/.*'
                                },
            'flixster':         {'seed': 'https://www.flixster.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://www.flixster.com/movie/.*'
                                },  
            'tribute':          {'seed': 'http://www.tribute.ca/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.tribute.ca/movies/.*'
                                },
            'boxofficemojo':    {'seed': 'http://www.boxofficemojo.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.boxofficemojo.com/movies/?id=.*'
                                },
            'mubi':             {'seed': 'https://mubi.com/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://mubi.com/films.*'
                                },
            'yify':             {'seed': 'http://yify.info/',
                                 'robots_txt': [],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://yify.info/.*'
                                }
}

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

FILES_PATH = os.path.join(os.getcwd() + '/files')
if not os.path.exists(FILES_PATH):
            os.makedirs(FILES_PATH)
            
MAX_PAGES = 5
        

class Crawler(threading.Thread):
    def __init__(self, website_name, website_info, use_heuristic=False):
        threading.Thread.__init__(self)
        self.website_name = website_name
        self.website_info = website_info
        self.use_heuristic = use_heuristic
        self.crawled_websites = []
        self.frontier = [website_info['seed']]
        self.visited = [website_info['seed']]
        self.stop_expanding = False
    
    
    def save_crawled_pages(self, results):
        results[self.website_name] = self.crawled_websites
        
        with open('results.pickle', 'wb') as f:
            pickle.dump(results, f)
    
    
    def expand_page(self, html_text):
        soup = BeautifulSoup(html_text, "lxml")
        
        # Expands the current URL to find more non-visited URLS
        for tag in soup.findAll('a', href=True):
            new_url = urljoin(self.website_info['seed'], tag['href'])
            # If the new URL is allowed by the robots_txt
            if new_url not in [urljoin(self.website_info['seed'], u) for u in self.website_info['robots_txt']]:
                # Within the seed domain and not visited yet
                if self.website_info['seed'] in new_url and new_url not in self.visited:
                    if self.use_heuristic:
                        # if it does not match the website_pattern, go to evaluate the next URL
                        if not re.match(self.website_info['movies_pattern'], new_url):
                            continue
                    
                    self.frontier.append(new_url)
                    self.visited.append(new_url)

                    if len(self.visited) >= MAX_PAGES:
                        self.stop_expanding = True
                        break
    
    
    def run(self):      
        while len(self.frontier) != 0:
            current_url = self.frontier.pop(0)
            
            time.sleep(self.website_info['sleep_time'])
                
            try:
                page = urllib2.Request(current_url, headers=USER_AGENT)
                page = urllib2.urlopen(page)
                html_text = page.read()
                
                # Checks if the type of the current URL is HTML
                r = requests.head(current_url)
                if "text/html" not in r.headers["content-type"]:
                    continue

            except Exception,e:
                print("\nERROR WITH URL: " + current_url)
                print("ERROR MESSAGE: " + e.message + '\n')
            
            self.crawled_websites.append(html_text)
            print(current_url)

            if not self.stop_expanding:
                self.expand_page(html_text)


def export_all_crawled_pages():
    with open('results.pickle', 'rb') as f:
        results = pickle.load(f)

    for website_name, crawled_pages in results.items():
        folder_path = os.path.join(FILES_PATH, website_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        count = 1
        for html_text in crawled_pages:
            file_complete_name = os.path.join(folder_path, website_name+'_'+str(count)+".html")
            with open(file_complete_name, "w") as f:
                f.write(html_text)
                count = count + 1
                
                
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
        
    
if __name__ == '__main__':
    crawl()
    export_all_crawled_pages()




