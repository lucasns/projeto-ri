from bs4 import BeautifulSoup
import cPickle as pickle
import re
import requests
import os
import threading
import time
import urllib2
from urlparse import urljoin

from config import DOMAINS, USER_AGENT, FILES_PATH


class Crawler(threading.Thread):
    def __init__(self, website_name, website_info, max_pages=500, use_heuristic=False):
        threading.Thread.__init__(self)
        self.website_name = website_name
        self.website_info = website_info
        self.use_heuristic = use_heuristic
        self.max_pages = max_pages
        self.crawled_websites = 0
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
        page = urllib2.Request(url, headers=USER_AGENT)
        page = urllib2.urlopen(page, timeout=5)
        html = page.read()

        return html


    def get_urls(self, html):
        soup = BeautifulSoup(html, "lxml")
        anchor_tags = soup.find_all('a', href=True)

        urls = [urljoin(self.website_info['seed'], link['href'].lower()) for link in anchor_tags]

        urls = [u for u in urls if (self.website_info['seed'] in u and
                                    u not in self.disallowed_links)]

        return urls


    def run(self):
        while len(self.frontier) > 0 and self.crawled_websites < self.max_pages:
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

                self.save_crawled_page(html)
                print(curr_url)

                for url in self.get_urls(html):
                    if url not in self.visited:
                        self.frontier.append(url)
                        self.visited.append(url)

            except Exception,e:
                print("\nERROR WITH URL: " + curr_url)
                print("ERROR MESSAGE: " + str(e.message) + '\n')


    def save_crawled_page(self, html):
        self.crawled_websites += 1

        path = FILES_PATH
        folder_path = os.path.join(path, self.website_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_complete_name = os.path.join(folder_path, self.website_name+'_'+str(self.crawled_websites)+".html")

        with open(file_complete_name, "w") as f:
            f.write(html)
