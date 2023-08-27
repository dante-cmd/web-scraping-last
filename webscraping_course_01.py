# -----------------------------------------------------------------
# Python Web Scraping - Second Edition -Fetching data from the web
# -------------- Katharine Jarmul - Richard Lawson ----------------
# -----------------------------------------------------------------

# 1. CHECK robot.txt
# Check the robot.txt file of the web side if has one.
# The robots.txt file is a valuable resource to check before crawling to minimize the chance of being
# blocked, and to discover clues about the website's structure
import json

target_site = r'https://www.mifarma.com.pe/'

# We must add /robots.txt
robots_site = target_site + '/robots.txt'

# In this web site we can find the sitemap
# Sitemap files are provided bywebsites to help crawlers locate their updated content without needing to
# crawl every web page.

site_map = 'https://inkafarma.pe/sitemap.xml'

# but need to be treated carefully
# because they can be missing, out-of-date, or incomplete.

# 2.  ESTIMATING THE SIZE OF A WEBSITE
# Search in Google, this a good proxy
# A quick way to estimate the size of a website is to check the results of Google's crawler

# Search in Google 'https://inkafarma.pe' -> Cerca de Cerca de 4,550,000 resultados.

# other advanced search parameters are available at http://www.google.com/advanced_search

# We can filter add precios
# https://inkafarma.pe/precios -> Cerca de 3,580,000 resultados

# 3. Identifying the technology used by a website -> Ask to Richard

# 4. Finding the owner of a website
# For some websites it may matter to us who the owner is. For example, if the owner is known to block
# web crawlers then it would be wise to be more conservative in our download rate.


import whois

print(whois.whois('appspot.com'))
print(whois.whois(target_site))  # to faramacias peruanas

# Google often blocks web crawlers despite being fundamentally a web crawling
# business themselves. We would need to be careful when crawling this domain because Google often
# blocks IPs that quickly scrape their services


# -----------------------------------------
# -------Crawling your first website-------
# -----------------------------------------

# In order to scrape a website, we first need to download its web pages containing the data of interest,
# a process known as crawling.
# There are a number of approaches that can be used to crawl a website,
# and the appropriate choice will depend on the structure of the target website

# 1. Crawling a sitemap
# 2. Iterating each page using database IDs
# 3. Following web page links

# ------------------------ Scraping versus crawling ---------------------------------------

# A WEB SCRAPER is built to access these specific pages and it will need to be
# modified if the site changes or if the information location on the site is changed

# CRAWLERS can be built to gather more specific information,
# but are usually used to crawl the web, picking up small and generic bits of information
# from many different sites or pages and following links to other pages

# -------------------------------------------------------------------------------------------

# 1. Download a web page
import requests
from requests import RequestException, HTTPError, ConnectionError, ConnectTimeout


def download(url):
    print('Downloading: ', url)
    try:
        html = requests.get(url).text
    except (RequestException, HTTPError, ConnectionError) as e:
        print('Download error: ', e.reason)
        html = None
    return html


# 1.1 Retrying downloads
# In this document (https://tools.ietf.org/html/rfc7231#section-6), we can see that

# *-- 4xx errors: occur when there is something wrong with our request and
# *-  5xx errors occur when there is something wrong with the server

def download(url, num_retries=2):
    print('Downloading:', url)
    try:
        html = requests.get(url)
        html.raise_for_status()  # Raise error when the content can't be read

    except (RequestException, HTTPError, ConnectionError, ConnectTimeout) as e:
        print('Download error:', e.response.status_code)

        html = None
        if num_retries > 0:
            if hasattr(e, 'response') and 500 <= e.response.status_code < 600:
                # hasattr return True if the object (e, in our case) contain the atributte 'code'
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


download(r'http://httpstat.us/500')  # test our function

# 2. SETTING A USER AGENT
# A user agent is a computer program representing a person, for example, a browser in a Web context.
# By default, request will download content with the python-requests/2.27.1
# some websites block this default user agent, this is the reason why We
# have to use an identifiable user agent

headers_default = requests.utils.default_headers()
headers_default['User-Agent']


# The best User-Agent to request Python
# User-Agent: Mozilla/5.0

def download(url, user_agent, num_retries=2):
    print('Downloading:', url)
    if not 'http:' in url:
        print('The web pag must contain http:..')
        return None
    else:
        try:
            html = requests.get(url, headers={'User-agent': user_agent})
            html.raise_for_status()  # Raise error when the content can't be read
            html = html.text

        except (RequestException, HTTPError, ConnectionError, ConnectTimeout) as e:
            print('Download error:', e.response.status_code)

            html = None
            if num_retries > 0:
                if hasattr(e, 'response') and 500 <= e.response.status_code < 600:
                    # hasattr return True if the object (e, in our case) contain the atributte 'code'
                    # recursively retry 5xx HTTP errors
                    return download(url, num_retries - 1)
        return html


download('http://www.meetup.com/', 'Mozilla/5.0')


# ---------------------------------------------------
# ----------------- Sitemap crawler------------------
# ---------------------------------------------------


def crawl_sitemap(url, user_agent):
    # download the sitemap file
    sitemap = download(url, user_agent)
    # extract link dfrom sitemap
    if isinstance(sitemap, (str, bytes)):
        links = re.findall('<loc>(.*?)</loc>', sitemap)
        for link in links:
            download(link, user_agent)


crawl_sitemap(site_map, 'Mozilla/5.0')  # Don't run

import requests, re
from bs4 import BeautifulSoup


def pyGooglSearch(word):
    word = 'farmacias peruanas'
    response = requests.get('https://www.google.com/search', params={'q': word})
    re.findall(r'.*(id=\w{5}).*', response.text)
    print(response.url)
    page = BeautifulSoup(response.content, 'html.parser')
    ws = page.find_all('div')
    ws
    Stats_results = page.find(id='result-stats')
    print(Stats_results)


pyGooglSearch('farmacias peruanas')

# -----------------------------------------------
# ----------------Link crawlers------------------
# ------------------------------------------------

# We could simply download the entire website by following every link. However, this would likely
# download many web pages we don't need

import re, requests
from requests import RequestException, HTTPError, ConnectionError, ConnectTimeout
from urllib.parse import urljoin


def get_links(html):
    """ Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a\shref=["'](.*?)["'][> ]""", re.I)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def link_crawler(start_url, link_regex, user_agent):
    """ Crawl from the given start URL following links matched by link_regex
    """
    crawl_queue = [start_url]
    none_type = type(None)

    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url, user_agent)

        if not isinstance(html, none_type):
            for link in get_links(html):
                # print(link := start_url + link) # A other way to do this is with urljoin

                link = urljoin(start_url, link)

                # If get_link don't match links
                # the loop don't inter
                if re.search(link_regex, link):
                    crawl_queue.append(link)


link_crawler('http://example.python-scraping.com', '/index|view/', 'Mozilla/5.0')  # don't run

from ndicts.ndicts import NestedDict

nd = NestedDict()
nd["level1", "level2", "level3"] = 0

# ---------------------------------------
# ---------- Advanced features ----------
# ---------------------------------------

# PARSING ROBOTS.TXT
# First, we need to interpret robots.txt to avoid downloading blocked URLs

from urllib import robotparser
import time

rfp = robotparser.RobotFileParser()
rfp.set_url(robots_site)
rfp.read()

user_agent = 'BadCrawler'
rfp.can_fetch(target_site, user_agent)


# an_fetch()function, which tells you
# whether a particular user agent is allowed to access a web page or not

# Integrating robotparser in crawl function

def get_robotparser(user_agent, url):
    rfp = robotparser.RobotFileParser()
    rfp.set_url(url + '/robots.txt')
    rfp.read()
    return rfp.can_fetch(url, user_agent)


def download(url, user_agent, num_retries=2):
    print('Downloading:', url)
    if not 'http:' in url:
        print('The web pag must contain http:..')
        return None
    else:
        if not get_robotparser(user_agent, url):  # Here we did the changes
            print('The User-Agent is not valid', user_agent)
        else:

            try:
                html = requests.get(url, headers={'User-agent': user_agent})
                html.raise_for_status()  # Raise error when the content can't be read
                html = html.text

            except (RequestException, HTTPError, ConnectionError, ConnectTimeout) as e:
                print('Download error:', e.response.status_code)

                html = None
                if num_retries > 0:
                    if hasattr(e, 'response') and 500 <= e.response.status_code < 600:
                        # hasattr return True if the object (e, in our case) contain the atributte 'code'
                        # recursively retry 5xx HTTP errors
                        return download(url, num_retries - 1)
            return html


link_crawler('http://example.python-scraping.com', '/index|view/', 'Mozilla/5.0')

# ***--------- SUPPORTING PROXIES -------------***
# A proxy server is a bridge between you and the rest of the internet.

from urllib.parse import urljoin


def download(url, user_agent, num_retries=2, prox=None):
    if not ('http:' in url):
        print('The web pag must contain http:..')
        return None
    else:
        if not get_robotparser(user_agent, url):  # Here we did the changes
            print('The User-Agent is not valid', user_agent)
        else:

            try:
                html = requests.get(url, headers={'User-agent': user_agent}, proxies=prox)
                html.raise_for_status()  # Raise error when the content can't be read
                html = html.text

            except (RequestException, HTTPError, ConnectionError, ConnectTimeout) as e:
                print('Download error:', e.response.status_code)

                html = None
                if num_retries > 0:
                    if hasattr(e, 'response') and 500 <= e.response.status_code < 600:
                        # hasattr return True if the object (e, in our case) contain the atributte 'code'
                        # recursively retry 5xx HTTP errors
                        return download(url, num_retries - 1)
            return html


def link_crawler(start_url, link_regex, user_agent, prox=None):
    """ Crawl from the given start URL following links matched by link_regex
    """
    crawl_queue = [start_url]
    none_type = type(None)
    time_init = time.time()
    critic_time = 5
    seen = [start_url]

    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url, user_agent, prox)
        actual_time = (time.time() - time_init)

        if actual_time < critic_time:

            if not isinstance(html, none_type):
                for link in get_links(html):

                    link = urljoin(start_url, link)

                    # If get_link don't match links
                    # the loop don't inter
                    if re.search(link_regex, link) and (link not in seen):
                        crawl_queue.append(link)
                        print(link)
                        seen.append(link)
        else:
            print('Sleeping 5 seconds')
            time.sleep(10)
            time_init = time.time()


# ** ----------Throttling downloads ---------------**
# If we crawl a website too quickly, we risk being blocked or overloading the server(s). To minimize
# these risks, we can throttle our crawl by waiting for a set delay between downloads

# We've incorporated the time to sleep in above

link_crawler('http://example.python-scraping.com', '/index|view/', 'Mozilla/5.0')  # don't run

time_init = time.time()
for i in range(3000000):

    actual_time = (time.time() - time_init)
    critic_time = 1

    if actual_time < critic_time:
        print(actual_time, i)
    else:
        print('Sleeping 5 seconds')
        time.sleep(10)
        time_init = time.time()

# AVOIDING SPIDER TRAPS
# To avoid download repeatly web pages
# I've incorporated in above, in my code

# PAG 111
# -------------------------------------------
# ----------- SCRAPING THE DATA -------------
# -------------------------------------------

# ---------------
# Beautiful Soup
# ----------------


import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from collections import namedtuple
import pandas as pd

# We will see how is the behavior of BeautifulSoup when the data is imcompleted

broken_html = '<ul class=country><li>Area<li>Population</ul>'
# parse the HTML
soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

# We can see it has used nested li elements, this was not hoped 
# we can try with html5lib in teh parser

soup = BeautifulSoup(broken_html, 'html5lib')
fixed_html = soup.prettify()
print(fixed_html)

# using html5lib was able to correctly interpret the missing attribute quotes and
# closing tags, as well as add the <html> and <body> tags to form a complete HTML document.
soup.find_all('ul', attrs={'class': 'country'})

# application to example

path_uk = r'http://example.python-scraping.com/places/default/view/United-Kingdom-233'
response = requests.get(path_uk)
page = BeautifulSoup(response.content, 'html5lib')
elements = page.find_all('tr', attrs={'id': re.compile(r'places.*')})

saved_list = []

for element in elements:
    if element:
        df = {}
        for c in element.find_all('td'):
            if c.label:
                label_text = c.label.text if c.label else None
                print(c.label.text)
                df['label'] = label_text

            elif c.img:
                img_link = urljoin(path_uk, c.img.get('src')) if c.img else None
                print(img_link)
                df['value'] = img_link

            elif c.text:
                text_extracted = c.text if c.text else None
                print(text_extracted)
                df['value'] = text_extracted

        saved_list.append(df)

data_saved = pd.DataFrame(saved_list)
data_saved.label = data_saved.label.str.replace(r':| ', '', regex=True)

# ------------
# --- Lxml----
# ------------
# is a Python library built on top of the libxml2 XML parsing library written in C, which helps
# make it faster than Beautiful Soup

from lxml.html import fromstring, tostring

broken_html = '<ul class=country><li>Area<li>Population</ul>'
# parse the HTML
tree = fromstring(broken_html)
fixed_html = tostring(tree, pretty_print=True)
print(fixed_html.decode())

# lxml was able to correctly parse the missing attribute quotes and closing tags,
# although it did not add the <html> and <body> tags. These are not requirements for standard XML and so
# are unnecessary for lxml to insert

path_uk = r'http://example.python-scraping.com/places/default/view/United-Kingdom-233'
response = requests.get(path_uk)
tree = fromstring(response.text)
td = tree.cssselect('tr#places_area__row>td.w2p_fw')[0]
td.text_content()

# for tr tag, that is, <tr id=places_area__row> ... <tr>
for tree_select_tr in tree.cssselect('tr'):
    # by each tr select all td in a list
    for tree_select_td in tree_select_tr.cssselect('td'):
        # by each td
        if tree_select_td.cssselect('img'):
            print(x := tree_select_td.cssselect('img[src*="png"]'))
            print(y := tostring(x[0]).decode())
            print(re.search(r'''src="(.*)"''', y).group(1))

## Here are some examples of common selectors

# Select any tag: *
# Select by tag <a>: a
# Select by class of "link": .link
# Select by tag <a> with class "link": a.link
# Select by tag <a> with ID "home": a#home
# Select by child <span> of tag <a>: a > span
# Select by descendant <span> of tag <a>: a span
# Select by tag <a> with attribute title of "Home": a[title=Home]

# Child => an immediate descendant of an ancestor (e.g. Joe and his father)
# Descendant => any element that is descended from a particular ancestor
# (e.g. Joe and his great-great-grand-father)

# -----------------
# XPath Selectors
# -----------------

# XPath is a way of describing relationships as a hierarchy in XML documents. Because HTML is
# formed using XML elements, we can also use XPath to navigate and select elements from an HTML
# document.

# Selector description | XPath Selector
# Select all links     |   '//a'
# Select div with class "main" | '//div[@class="main"]'
# Select ul with ID "list" | '//ul[@id="list"]'
# Select text from all paragraphs | '//p/text()'
# Select all divs which contain 'test' in the class | '//div[contains(@class, 'test')]'
# Select all divs with links or lists in them | '//div[a|ul] '
# Select a link with google.com in the href | '//a[contains(@href, "google.com")]
# Get specifically data from src '//td/img/(@src'

path_uk = r'http://example.python-scraping.com/places/default/view/United-Kingdom-233'
response = requests.get(path_uk)
tree = fromstring(response.text)
print(tostring(tree).decode())

td = tree.xpath('//tr[@id="places_area__row"]/td[@class="w2p_fw"]/text()')
print(td)

elements = tree.xpath('//td/img')

for element in elements:
    print(element.get('src'))

# we can pass this in the console $x('//tr[@id="places_area__row"]/td[@class="w2p_fw"]/text()')

# -------------------------------------------
# ----------LXML and Family Trees -----------
# -------------------------------------------

# Every element on a web page can have parents, siblings and children.
# These relationships can help us more easily traverse the page.

path_uk = r'http://example.python-scraping.com/places/default/view/United-Kingdom-233'
response = requests.get(path_uk)
tree = fromstring(response.text)

element = tree.xpath("//table")[0]  # there is an element.
print(element.getchildren())  # all children of table

element.getprevious()  # get previous sibling
element.getnext()  # get next sibling
element.getparent()  # get parent

# ------------------------
# Concurrent Downloading
# ------------------------

# We need to download multiple web pages simultaneously.


from zipfile import ZipFile
from io import BytesIO, TextIOWrapper
import requests
from pathlib import Path
import numpy as np

class AlexaCallback:

    def __init__(self, max_urls=500):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self):
        response = requests.get(self.seed_url)

        with ZipFile(BytesIO(response.content)) as zf:
            # response.content is in bytes, but the parser must be in IO bytes
            zf.printdir()  # print the files inside zip file.
            csv_namefile = zf.namelist()[0]  # choose the name of the file

            with zf.open(csv_namefile) as csv_file:
                data_csv = csv_file.read().decode()
                data_url = re.findall(r'\d*\,(.*)', data_csv, re.MULTILINE)
                np.random.seed(123)
                data_url = np.random.choice(data_url, self.max_urls)

        return data_url


alexa = AlexaCallback(max_urls=10)
data_url = alexa()

import requests
import time
import concurrent.futures
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json


def page_html(link: str):

    try:
        response = requests.get('http://' + link)
        response.raise_for_status()

        if response.status_code == 200:
            path_init = Path()
            name_link = re.search(r'(.*?)\..*', link).group(1)
            if not (path_init / 'data_page').exists():
                (path_init / 'data_page').mkdir()

            if not (path_init / 'data_page' / f'{name_link}.json').exists():
                with open(path_init / 'data_page' / f'{name_link}.json', 'w') as writer:
                    json.dump({name_link:response.text},writer)
                    print('donwload: ', link)
    except:
        print('Error in: ',link)

t1 = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(page_html, data_url)

t2 = time.perf_counter()
print(f'Finished in {t2 - t1} seconds')


