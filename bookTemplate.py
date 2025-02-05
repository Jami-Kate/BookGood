import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def cleanup(str):
    str = re.sub('\[\^\]', '', str)
    return str


cuckoo = 'https://www.whsmith.co.uk/Product/Gretchen-Felker-Martin/Cuckoo/13100619?_gl=1*1a671yr*_up*MQ..*_ga*Nzg3ODUxNzAwLjE3MzgzMjI2Nzk.*_ga_9YDXQFM2GM*MTczODMyMjY3OC4xLjAuMTczODMyMjY3OC4wLjAuMTA1NDI3NTE3Ng..'
pote = 'https://www.whsmith.co.uk/Product/Ken-Follett/The-Pillars-of-the-Earth/11576358?_gl=1*1nq3jo4*_up*MQ..*_ga*MjA2OTY3ODg1NC4xNzM4NzQ1Nzc0*_ga_9YDXQFM2GM*MTczODc0NTc3My4xLjAuMTczODc0NTc3My4wLjAuNDk1OTc2NjM1'

session = requests.Session()
r = session.get(pote)

options = webdriver.ChromeOptions()
options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

dr = webdriver.Chrome(
    options=options
    )
dr.get(pote)

soup = BeautifulSoup(dr.page_source, 'html.parser')
description = soup.find('div', class_ = 'summary')
details = soup.find_all('div', class_ = 'details')

print(cleanup(details[1].text.strip()))

