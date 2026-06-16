import sys # for argv list
import argparse # to parse arguments
import requests # for HTTP requets
from bs4 import BeautifulSoup # to parse HTML text
from urllib.parse import urljoin # to build absolute URLs from relative ones
from urllib.parse import urlparse # to decompose a URL into its components (scheme, path, query...)
import os

# Command line arguments parsing
parser = argparse.ArgumentParser(description='Scrap images from a website')
parser.add_argument('url', type=str, help='the URL of the website')
parser.add_argument('-r', action="store_true", help='recursively downloads the images in the given URL')
parser.add_argument('-l', type=int, default=None, help='indicates the maximum depth level of the recursive download. 5 by default')
parser.add_argument('-p', type=str, default='./data/', help='indicates the path where the downloaded files will be saved. ./data/ by default')

# Parses the command line arguments and stores them in the args variable.
args = parser.parse_args()

# Checks if the -r option exists when the -l option is called.
if args.l is not None and not args.r:
	print('The -l option cannot be called without the -r option.')
	sys.exit(1)

# If the -r option exists and the -l option is not defined, set the maximum depth level to 5.
if args.l is None and args.r:
	args.l = 5

# Creates the directory where the images will be saved if it does not exist.
try:
	os.makedirs(args.p, exist_ok=True)
except OSError:
	print('Cannot create directory')
	sys.exit(1)

# Gets the base domain of the given URL to check if the links found in the page are in the same domain.
# If the -l option is not defined, set the initial depth level to 0. Otherwise, set it to the value of the -l option.
# Set to keep track of visited URLs to avoid infinite loops in recursive scraping.
# Set of authorized image extensions to filter the images to be downloaded.
base_domain = urlparse(args.url).netloc
initial_depth_level = 0 if args.l is None else args.l
visited = set()
authorized_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

# Scrapes the given URL and downloads the images found in it.
# If the -r option is called, it recursively scrapes the links found in the page until the maximum depth level is reached.
def scrape(url, depth_level, already_visited):

	if url in already_visited: return
	already_visited.add(url) 

	# HTTP GET request (returns a Response object).
	try:
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		if page.status_code >= 400:
			if url == args.url:
				print('The HTTP request failed for the first URL.')
				sys.exit(1)
			else:
				print(f'The HTTP request failed for: {url}.')
				return
	except requests.exceptions.RequestException:
		if url == args.url:
			print('Exception raised in HTTP request for the first URL.')
			sys.exit(1)
		else:
			print(f'Exception raised in HTTP request for: {url}.')
			return

	# Parse the html.text attribute of the Response object to build a usable BeautifulSoup object.
	soup = BeautifulSoup(page.text, 'html.parser')

	# For each <img> tag:
	# gets the value of 'src'
	# builds an absolute URL if necessary
	# extracts the image path and then its extension to check its validity
	# gets the image data
	# builds the path where the image will be written
	# writes the image binary data to the destination file
	for image in soup.find_all('img'):
		src = image.get('src')
		if src is None:
			continue
		img_url = urljoin(url, src)
		parsed_url = urlparse(img_url)
		extension = os.path.splitext(parsed_url.path)[1].lower()
		if extension not in authorized_extensions:
			continue
		try:
			img_downloaded = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
			if img_downloaded.status_code >= 400:
				print('The image GET request failed.')
				continue
		except requests.exceptions.RequestException:
				print('Exception raised in the image GET request.')
				continue
		img_name = os.path.basename(parsed_url.path)
		img_path = os.path.join(args.p, img_name)
		try:
			with open(img_path, 'wb') as file:
				file.write(img_downloaded.content)
		except OSError:
			print('Exception raised in the image writing.')
			continue

	# If the -r option is called and the depth level is greater than 0, for each <a> tag:
	# gets the value of 'href'
	# builds an absolute URL if necessary
	# checks if the link is in the same domain as the base URL
	if args.r and depth_level > 0:
		for link in soup.find_all('a'):
			href = link.get('href')
			if href is None:
				continue
			absolute_href = urljoin(url, href)
			if urlparse(absolute_href).netloc == base_domain:
				print(f'Going to scrape: {absolute_href}')
				scrape(absolute_href, depth_level - 1, already_visited)

# Start the scraping process
scrape(args.url, initial_depth_level, visited)
