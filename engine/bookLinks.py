#from requests_html import HTMLSession
import lxml_html_clean

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

url = 'https://www.whsmith.co.uk/Search/Books/Next-90-Days/5-Star?fq=01120-0319-4135&sort=Bestselling&pg=1'

session = requests.Session()
r = session.get(url)


dr = webdriver.Chrome()
dr.get(url)

soup = BeautifulSoup(dr.page_source, 'html.parser')
print(soup.find('div', class_ = 'search-item__image'))