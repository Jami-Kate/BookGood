import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time

class LinkManager: 
    def __init__(self): 
        self.links = []
        self.details = []

def LMnger(): 
    return LinkManager() 

def book_links():
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
    
    return links


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

def first_retrieval(linkFile, bookDetsFile):
    i = 0
    while i < 30:
        bookDetsFile[i] = get_book(linkFile[i])
        i += 1

    if os.path.exists("../data/data.json"):
        os.remove("../data/data.json")
    file = open('../data/data.json','w')
    
    json.dump(bookDetsFile, file, indent = 4)

    return bookDetsFile


def retrieve_more(linkFile, bookDetsFile, ind):
    startInd = 30 * ind
    endInd = 30 * (ind + 1)

    if startInd >= len(linkFile):
        return bookDetsFile
    
    while startInd < endInd:
        bookDetsFile[startInd] = get_book(linkFile[startInd])
        startInd += 1
    
    print(startInd)
    print(endInd)

    if os.path.exists("../data/data.json"):
        os.remove("../data/data.json")
    file = open('../data/data.json','w')
    
    json.dump(bookDetsFile, file, indent = 4)

    return bookDetsFile


