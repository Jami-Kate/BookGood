import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

def cleanup(str):
    str = re.sub('\[\^\]', '', str)
    return str

pote = 'https://www.whsmith.co.uk/Product/Ken-Follett/The-Pillars-of-the-Earth/11576358?_gl=1*vnxb4b*_up*MQ..*_ga*MTc1ODI1MzIwNC4xNzM4ODM0NjQz*_ga_9YDXQFM2GM*MTczODgzNDY0Mi4xLjAuMTczODgzNDY0Mi4wLjAuNjg0Mjc0NDE3'

cuckoo = 'https://www.whsmith.co.uk/Product/Gretchen-Felker-Martin/Cuckoo/13100619?_gl=1*1a671yr*_up*MQ..*_ga*Nzg3ODUxNzAwLjE3MzgzMjI2Nzk.*_ga_9YDXQFM2GM*MTczODMyMjY3OC4xLjAuMTczODMyMjY3OC4wLjAuMTA1NDI3NTE3Ng'

def get_book(book_url):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    dr = webdriver.Chrome(
        options=options
        )
    dr.get(book_url)

    soup = BeautifulSoup(dr.page_source, 'html.parser')
    title = soup.find('h1', itemprop = 'name').contents[0].text.strip()
    author = soup.find('span', itemprop = 'name').contents[0].text.strip()
    category = soup.find('ul', class_ = 'breadcrumb__list').contents[-1].text.strip()
    details = soup.find_all('div', class_ = 'details')[1].text.strip()

    return {'title' : title, 'author' : author, 'category' : category, 'details' : cleanup(details)}

test = get_book(pote)

print(test['title'])
print(test['author'])
print(test['category'])
print(test['details'])