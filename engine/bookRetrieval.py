import requests
from bs4 import BeautifulSoup
import re
import json
import os

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

# Data to be written
dictionary = {
    "name": "sathiyajith",
    "rollno": 56,
    "cgpa": 8.6,
    "phonenumber": "9976770500"
}
 
# Serializing json
json_object = None


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

if os.path.exists("../data/data.json"):
  os.remove("../data/data.json")

file = open('../data/data.json','w')
'''
def write_json(new_data):
    with open('../data/data.json','r+') as file:

        # First we load existing data into a dict.
        if len(file) == 0:
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        else:
            json.dump(new_data, indent = 4)
'''
for link in links:
    bookDets[i] = get_book(link)
    i += 1



json.dump(bookDets, file, indent = 4)

 
