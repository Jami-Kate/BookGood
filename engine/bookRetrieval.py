import requests
from bs4 import BeautifulSoup
import re

url = f'https://www.bookreporter.com/coming-soon'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

linksTemp = soup.find_all('div', class_ = 'book-info')

i = 1
while i < 6:
    url = f'https://www.bookreporter.com/coming-soon?page={i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    temp2 = soup.find_all('div', class_ = 'book-info')
    for tem in temp2:
        linksTemp.append(tem)
    i += 1

links = [] * len(linksTemp)

for linkie in linksTemp:
    linkTemp = linkie.find('a')
    link = linkTemp['href']
    links.append('https://www.bookreporter.com' + link)

bookDets = [""] * (len(links))

def get_book(book_url):

    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h2', id = 'page-title').find('a').text.strip()
    author = soup.find('div', id = 'author').find('a').text.strip()
    category = soup.find('div', id = 'book-data').find_all(href=re.compile("/genres/"))
    
    i = 0
    while i < len(category):
        cow = category[i].text.strip()
        category[i] = cow
        i += 1
    
    details = soup.find('div', id = 'review').find_all('p')
    i = 0
    review = ""
    while i < len(details):
        review = review + " " + details[i].text.strip()
        i += 1

    return {'title' : title, 'author' : author, 'genres' : category, 'review' : review}

i = 0
for link in links:
    bookDets[i] = get_book(link)
    i += 1

print(bookDets)
 
