import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

def cleanup(str):
    str = re.sub('\[\^\]', '', str)
    return str

def get(book_url):

    session = requests.Session()
    r = session.get(book_url)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    dr = webdriver.Chrome(
        options=options
        )
    dr.get(book_url)

    soup = BeautifulSoup(dr.page_source, 'html.parser')
    details = soup.find_all('div', class_ = 'details')

    return cleanup(details[1].text.strip())

