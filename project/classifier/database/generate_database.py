import urlparse
import urllib2
import re
import time
import cPickle as pickle

from nltk.corpus import stopwords
from bs4 import BeautifulSoup


LINK_FILES = ["boxofficemojo.txt", "rotten.txt", "imdb.txt", "metacritic.txt", "movies.txt", "allmovies.txt", "flixter.txt", "tribute.txt", "mubi.txt", "yifi.txt"]
STOPWORDS = set(stopwords.words("english"))

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def clean_text(text):
	letters_only = re.sub("[^a-zA-Z]", " ", text)
	words = letters_only.lower().split()
	meaningful_words = [w for w in words if not w in STOPWORDS]
	return " ".join(meaningful_words)


def extract_text(html):
	def visible(element):
		if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
			return False
		elif re.match('<!--.*-->', str(element.encode('utf-8'))):
			return False
		else:
			return True

	soup = BeautifulSoup(html, 'html.parser')
	data = soup.findAll(text=True)
	all_text = ''.join(filter(visible, data))
	text = all_text.replace('\n', ' ').replace('\r', '').strip()
	text = ' '.join(text.split())
	text = clean_text(text)

	return text


def format_link(url):
	if url[-1] == '\n':
		return url[:-1]
	else:
		return url


def get_links(filename):
	print "Reading links from file '%s'" % filename

	f = open(filename, 'r')
	links = {'positive':[], 'negative':[]}

	for i in range(15):
		url = format_link(f.readline())
		links['positive'].append(url)

	for i in range(15):
		url = format_link(f.readline())
		links['negative'].append(url)

	f.close()

	return links



def get_page_content(url):
	print "# Retrieving contents from url: %s" % url
	page = urllib2.Request(url, headers=USER_AGENT)
	page = urllib2.urlopen(page)
	html_text = page.read()
	content = extract_text(html_text)
	time.sleep(1)
	return content


def download_pages():
	database = {}

	for filename in LINK_FILES:
		links = get_links('links/' + filename)
		database[filename] = {'positive':[], 'negative': []}

		print "> Retrieving positive pages"
		for p in links['positive']:
			content = get_page_content(p)
			database[filename]['positive'].append(content)

		print "> Retrieving negative pages"
		for n in links['negative']:
			content = get_page_content(n)
			database[filename]['negative'].append(content)

	db_file = open('database.pickle', 'wb')
	pickle.dump(database, db_file, pickle.HIGHEST_PROTOCOL)
	db_file.close()


if __name__ == '__main__':
	download_pages()
