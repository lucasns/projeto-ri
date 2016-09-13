import urlparse
import urllib
import requests
from bs4 import BeautifulSoup

domains = ["https://www.rottentomatoes.com/",
			"http://www.imdb.com/",
			"https://play.google.com/store/movies/",
			"http://www.metacritic.com/",
			"http://www.allmovie.com/",
			"http://www.tribute.ca/",
			"http://www.boxofficemojo.com/",
			"http://www.rogerebert.com/",
			"http://www.comingsoon.net/",
			"http://www.movies.com/",
			"https://www.flixster.com/",
			"http://www.cinemablend.com/"]

for domain in domains:
	urls = [domain]
	visited = [domain]

	count = 1
	stop_expanding = False
	max_pages = 5
	website_name = urlparse.urlparse(domain).hostname.split('.')[1]

	while len(urls) != 0:	
		try:
			page = urllib.urlopen(urls[0])
			html_text = page.read()

		except:
			print("Error: " + urls[0])

		# Saves the html text as a file
		with open(website_name + '_' + str(count) + ".html", "w") as text_file:
			text_file.write(html_text)
			count = count + 1

		# Removes saved html link from queue
		print(urls.pop(0))

		if not stop_expanding:
			soup = BeautifulSoup(html_text, "lxml")

			# Expands actual url to find more non-visited urls
			for tag in soup.findAll('a', href=True):
				tag['href'] = urlparse.urljoin(domain, tag['href'])

				# Same domain and not visited
				if domain in tag['href'] and tag['href'] not in visited:
					urls.append(tag['href'])
					visited.append(tag['href'])

					if len(visited) == max_pages:
						stop_expanding = True
						break




