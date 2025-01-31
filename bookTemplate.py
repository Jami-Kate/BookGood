#from requests_html import HTMLSession
import lxml_html_clean

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

url = 'https://www.whsmith.co.uk/Product/Gretchen-Felker-Martin/Cuckoo/13100619?_gl=1*1a671yr*_up*MQ..*_ga*Nzg3ODUxNzAwLjE3MzgzMjI2Nzk.*_ga_9YDXQFM2GM*MTczODMyMjY3OC4xLjAuMTczODMyMjY3OC4wLjAuMTA1NDI3NTE3Ng..'

session = requests.Session()
r = session.get(url)


dr = webdriver.Chrome()
dr.get(url)

soup = BeautifulSoup(dr.page_source, 'html.parser')
print(soup.find('div', class_ = 'summary'))

