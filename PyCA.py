########################################################################
# ------------------- Python Automation Cookbook -----------------------
########################################################################

# ------------------------------
# 1. Sending email notifications
# -------------------------------

# This approach is viable for spare emails sent to a couple of people, as a result
# of an automated task, but no more than that

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def main(to_email, server, port, from_email, password, subject, text):
    print(f'With love, from {from_email} to {to_email}')

    # create the message

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add Text
    msg.attach(MIMEText(text, 'plain'))
    with open(r'C:\Users\LENOVO\Desktop\python_course\datascience\WEBSCRAP\pika.png', 'rb') as reader:
        img_pika = reader.read()
        msg.attach(MIMEImage(img_pika), )

    # Create SMTP session for sending the mail
    session = smtplib.SMTP(server, port)
    session.starttls()  # enable security
    session.login(from_email, password)
    msg_in = msg.as_string()
    session.sendmail(from_email, to_email, msg_in)
    session.quit()
    print('Login Success')


main(to_email='dante.toribio@unmsm.edu.pe',
     server='smtp.gmail.com',
     port=587,
     from_email='danteca.dtc@gmail.com',
     password='4249245+Dtc',
     subject='With love, from ME to You',
     text='''Hola Dante
     Muchas gracias por haber participado en nuestro proceseo pero continuamos
     con otro''')

# -------------------------------------------------------
# --------------------WEB SCRAPING-----------------------
# -------------------------------------------------------

import requests
import re

path_col = 'http://www.columbia.edu/~fdc/sample.html'

response = requests.get(path_col)  # get file from url
print(response.status_code)  # Print status
response.text  # if the url is web page, this return the web page in str type
response.request.headers  #
response.headers['content-type']  # to get the content-type of the web page

# If we made a bad request
# a 4XX client error or 5XX server error response
path_col_fail = 'http://www.columbia.edu/invalid'
response_fail = requests.get(path_col_fail)
response_fail.status_code
response_fail.raise_for_status()

# If we made a good request The .raise_for_status() is None
type(response.raise_for_status())

# Downloading raw text or a binary file is a good starting point, but the main language
# of the web is HTML.

# HTML is a structured language, defining different parts of a document such as
# headings and paragraphs. HTML is also hierarchical, defining sub-elements. The
# ability to parse raw text into a structured document is basically the ability to extract
# information automatically from a web page. For example, some text can be relevant
# if enclosed in certain HTML elements, such as a class div or after a heading h3 tag.

import requests
from bs4 import BeautifulSoup

# Beautiful Soup is a Python library for pulling data out (estract data) of HTML and XML files.
# It works with your favorite parser (request) to provide idiomatic ways of navigating, searching, and modifying the parse tree

URL = 'http://www.columbia.edu/~fdc/sample.html'
response = requests.get(URL)
response.status_code
response.headers['Content-Type']
page = BeautifulSoup(response.text, 'html.parser')  # response.text is the extracted text from request

print(page.prettify())  # To see the structure of page

page.title  # title is part of the structure, tag
page.title.name  # name of the tag, in this case title
page.title.string  # string between <title> ... </title>
page.title.parent.name  # The parent tag
page.title.parent

page.find_all('h3')  # fin all objects with tags <h3> ... </h3>

# each h3 has unique id and we choose the convert
link_section = page.find('h3', attrs={'id': 'convert'})

section = []
for element in link_section.next_elements:  # all the next elements
    if element.name == 'h3':  # the for loop stop when the next heading h3 is passed.
        print(element)
        break
    if element.name == 'a':
        print(element.get('href'))
    section.append(element.string or '')

result = ''.join(section)
print(result)

# for install
# html5lib
# lxml


# ------------------------------------
# -------- Crawling the web ----------
# ------------------------------------
# Crawl a web is search from a link parent other links that likely contains
# information that We need.
# The goal is match all links that contains the informations we need, and after
# save them in a list.

# The full script, crawling_web_step1.py, is available on GitHub at
# the following link: https://github.com/PacktPublishing/Python-
# Automation-Cookbook-Second-Edition/blob/master/Chapter03/
# crawling_web_step1.py


import argparse
import requests
import logging
import http.client
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

DEFAULT_PHRASE = 'python'


def process_link(source_link, text):
    logging.info(f'Extracting links from {source_link}')
    parsed_source = urlparse(source_link)
    result = requests.get(source_link)
    if result.status_code != http.client.OK:
        logging.error(f'Error retrieving {source_link}: {result}')
        return []

    if 'html' not in result.headers['Content-type']:
        logging.info(f'Link {source_link} is not an HTML page')
        return []

    page = BeautifulSoup(result.text, 'html.parser')
    search_text(source_link, page, text)

    return get_links(parsed_source, page)


def get_links(parsed_source, page):
    '''Retrieve the links on the page'''
    links = []
    for element in page.find_all('a'):
        link = element.get('href')
        if not link:
            continue

        # Avoid internal, same page links
        if link.startswith('#'):
            continue

        if link.startswith('mailto:'):
            # Ignore other links like mailto
            # More cases like ftp or similar may be included here
            continue

        # Always accept local links
        if not link.startswith('http'):
            netloc = parsed_source.netloc
            scheme = parsed_source.scheme
            path = urljoin(parsed_source.path, link)
            link = f'{scheme}://{netloc}{path}'

        # Only parse links in the same domain
        if parsed_source.netloc not in link:
            continue

        links.append(link)

    return links


def search_text(source_link, page, text):
    '''Search for an element with the searched text and print it'''
    for element in page.find_all(text=re.compile(text, flags=re.IGNORECASE)):
        print(f'Link {source_link}: --> {element}')


def main(base_url, to_search):
    checked_links = set()
    to_check = [base_url]
    max_checks = 10

    while to_check and max_checks:
        link = to_check.pop(0)
        links = process_link(link, text=to_search)
        checked_links.add(link)
        for link in links:
            if link not in checked_links:
                checked_links.add(link)
                to_check.append(link)

        max_checks -= 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='url', type=str,
                        help='Base site url. '
                             'Use  "http://localhost:8000/" '
                             'for the recipe example')
    parser.add_argument('-p', type=str,
                        help=f'Sentence to search, default: {DEFAULT_PHRASE}',
                        default=DEFAULT_PHRASE)
    args = parser.parse_args()

    main(args.url, args.p)

###########################################################################
###########################################################################
###########################################################################
# -----------------------------------------------------------------
# -------------------- SELENIUM ----------------------------------
# -----------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_path = r'C:\dchrome\chromedriver.exe'
ser = Service(driver_path)
opt = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=ser, options=opt)
browser.get('https://httpbin.org/forms/post')
custname = browser.find_element(by=By.NAME, value='custname')

custname.clear()
custname.send_keys("Sean O'Connell")

for size_element in browser.find_elements(by=By.NAME, value='size'):
    if size_element.get_attribute('value') == 'medium':
        print(size_element.is_enabled())
        size_element.click()

for topping in browser.find_elements(by=By.NAME, value='topping'):
    if topping.get_attribute('value') in ['bacon', 'cheese']:
        topping.click()

browser.find_element(by=By.TAG_NAME, value='form').submit()
browser.quit()

# --------------------------------------
# --------------------------------------
# --------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver_path = r'C:\dchrome\chromedriver.exe'
ser = Service(driver_path)

chrome_options = webdriver.ChromeOptions()
# add argument to not displayed
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options, service=ser)
browser.get("https://httpbin.org/forms/post")
browser.save_screenshot('screenshot.png')

# -------------------------------------------------------------------------------------
# -------------------- Accessing password-protected pages -----------------------------
# -------------------------------------------------------------------------------------

import requests

requests.get('http://httpbin.org/basic-auth/user/psswd', auth=('user', 'psswd'))

# Use the wrong credentials to return a 401 status
requests.get('http://httpbin.org/basic-auth/user/psswd', auth=('user', 'wrong'))

# The credentials can also be passed directly as part of the URL, separated by a
# colon and an @ symbol before the server, like this:
requests.get('https://user:psswd@httpbin.org/basic-auth/user/psswd')

# using urljoin, urlparse
import re
from urllib.parse import urljoin, urlparse

url_source = urlparse(r'https://larepublica.pe/programas')
url_pe = r'/programas/carlincaturas-en-video/carlincatura-de-hoy-sabado-26-de-marzo-de-2022-no-es-valida-9659'
url_source.scheme
url_source.netloc
url_source.path

path = urljoin(url_source.path, url_pe)
link = f'{url_source.scheme}://{url_source.netloc}{path}'
print(link)

# --------------  concurrent -----------------
import requests
import time
import concurrent.futures
from pathlib import Path

img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]

path_init = Path(exist_ok=True, parent=True)
if not (path_init / 'img').exists():
    (path_init / 'img').mkdir()

t1 = time.perf_counter()


def download_image(img_url):
    img_name = img_url.split('/')[3]
    if not (path_init / 'img' / img_name).exists():
        img_bytes = requests.get(img_url).content
        img_name = f'{img_name}.jpg'
        with open(path_init / 'img' / img_name, 'wb') as img_file:
            img_file.write(img_bytes)
            print(f'{img_name} was downloaded...')


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)

t2 = time.perf_counter()
print(f'Finished in {t2 - t1} seconds')

############################################################
# ###############################################################3
# To download images with BSP4 
# https://medium.com/geekculture/scrape-google-images-with-python-f9a20cda1355


# ------------------------------------------------------
# ------------Speeding up web scraping -----------------
# ------------------------------------------------------

# we will see how to download a list of pages in parallel and wait until they are all ready

def dowload_files_treasury(name_type, year):

    from urllib.parse import urlparse
    import requests
    from bs4 import BeautifulSoup
    from pathlib import Path

    path_treasury = r'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2022'
    path_treasury_parse = urlparse(path_treasury)
    path_treasury_init = path_treasury_parse.scheme + '://' + path_treasury_parse.netloc + path_treasury_parse.path

    query = f'?q={name_type}&field_tdr_date_value={year}'
    path_treasury_init_1 = path_treasury_init + query
    response = requests.get(path_treasury_init_1) #params={'q': [name_type, year]}

    total_size  = response.headers.get('content-length')

    page = BeautifulSoup(response.content, 'html.parser')
    elements = page.find_all('div', attrs={'class': re.compile('.*csv.*')})
    for element in elements:
        url = element.a.get('href')
        name_file = re.search(r'.*\/(.*\.csv).*', url).group(1)
        name_file_final = f'{year}-{name_file}'
        response_url = requests.get(url)
        path_init = Path(parents=True, exist_ok=True)
        if not (path_init/name_type).exists():
            (path_init / name_type).mkdir()

        with open((path_init / name_type/name_file_final), 'wb') as writer:
            writer.write(response_url.content)
            print(f'Se está descargando {name_file_final} size {total_size}')
        if (path_init / name_type/name_file_final):
            pass


def dowload_files_treasury_1(name_type, year):

    from urllib.parse import urlparse
    import requests
    from bs4 import BeautifulSoup
    from pathlib import Path

    path_treasury = r'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2022'
    path_treasury_parse = urlparse(path_treasury)
    path_treasury_init = path_treasury_parse.scheme + '://' + path_treasury_parse.netloc + path_treasury_parse.path

    query = f'?q={name_type}&field_tdr_date_value={year}'
    path_treasury_init_1 = path_treasury_init + query
    response = requests.get(path_treasury_init_1) #params={'q': [name_type, year]}

    total_size  = response.headers.get('content-length')

    page = BeautifulSoup(response.content, 'html.parser')
    elements = page.find_all('div', attrs={'class': re.compile('.*csv.*')})
    for element in elements:
        url = element.a.get('href')
        name_file = re.search(r'.*\/(.*\.csv).*', url).group(1)
        name_file_final = f'{year}-{name_file}'
        response_url = requests.get(url)
        path_init = Path(parents=True, exist_ok=True)
        if not (path_init/name_type).exists():
            (path_init / name_type).mkdir()

        with open((path_init / name_type/name_file_final), 'wb') as writer:
            chunks = 0
            for chunk in response_url.iter_content(chunk_size=1024):
                chunk
                if chunk:
                    chunks += 1
                    downloaded = chunks * 1024
                    # An approximation as the chunks don't have to be 512 bytes
                    progress = int((downloaded / int(total_size)) * 100)
                    print(f"\r Download Progress {progress} %", end='')
                    writer.write(chunk)
            print("\nFinished")

            #writer.write(response_url.content)
            #print(f'Se está descargando {name_file_final} size {total_size}')

name_type = 'daily_treasury_yield_curve'
year = 2022
dowload_files_treasury_1(name_type, year)


import  time

for i in range(50):
    time.sleep(0.1)
    guion = '-'*(50-1 -i)
    igual = '='*(i)+'>'
    to_print = f'\r [{igual}{guion}] {round((i/49)*100)}%'
    print(to_print, end='')

