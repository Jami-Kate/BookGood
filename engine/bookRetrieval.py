import requests
from bs4 import BeautifulSoup
import re
import json
import os
import hashlib

def book_links():
    '''Initial link pages'''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Referer': 'https://www.bookreporter.com/coming-soon',
    'Accept-Language': 'en-US,en;q=0.9'} # to pass the turing test

    url = f'https://www.bookreporter.com/coming-soon'
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    linksTemp = soup.find_all('div', class_ = 'book-info')

    '''Iterate next 5 pages for links; retrieves 150 total'''
    i = 1
    while i < 6:
        url = f'https://www.bookreporter.com/coming-soon?page={i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        temp2 = soup.find_all('div', class_ = 'book-info')
        for tem in temp2:
            linksTemp.append(tem)
        i += 1

    '''Intialize an array to store links, get links'''
    links = [] * len(linksTemp)

    for linkie in linksTemp:
        linkTemp = linkie.find('a')
        link = linkTemp['href']
        links.append('https://www.bookreporter.com' + link)
    
    '''Store the links in the links.json file'''
    if links:
        with open('static/data/links.json', 'w') as link_file:
            json.dump({"pointer": 0, "links": links}, link_file, indent=4)
        print(f"Successfully fetched {len(links)} book links!")
    else:
        print("No links found.")
    return 


'''Given a url to a book, retrieves the details of that book'''
def get_book(book_url):

    '''runs beautiful soup on the url'''
    response = requests.get(book_url, verify=False) 
    soup = BeautifulSoup(response.content, 'html.parser')
    
    '''retrieves the relevant details'''
    title = soup.find('h2', id = 'page-title').find('a').text.strip()
    author = soup.find('div', id = 'author').find('a').text.strip()
    
    '''creates a unique integer ID based on hashed title + author'''
    hashedTitle = (title + author).encode('utf-8')
    hashedTitle = int(hashlib.sha224(hashedTitle).hexdigest(),base=16)


    '''Strips the genres down to just and array of the text of the genre'''
    category = soup.find('div', id = 'book-data').find_all(href=re.compile("/genres/"))
    i = 0
    while i < len(category):
        cow = category[i].text.strip()
        category[i] = cow
        i += 1
    
    '''Strips the review down to just text of the review, no links or paragraph breaks'''
    details = soup.find('div', id = 'review').find_all('p')
    i = 0
    review = ""
    while i < len(details):
        review = review + " " + details[i].text.strip()
        i += 1

    '''Returns in a format for JSON'''
    return {'title' : title, 'author' : author, 'id' : hashedTitle, 'genres' : category, 'review' : review, 'mood' : None}


'''Helper Function to put new books and metadata into the data.json file'''
def dumpToJSON(dataIn, metaIn):
    
    '''if the file already exists and has data, removes that data and stores it
       then it deletes the JSON to put in new data'''
    if os.path.exists("static/data/data.json"):
        # f = open('static/data/data.json')
        f = 'static/data/data.json'
        with open(f, 'r') as data_file:
            dataOut = json.load(data_file)
        #adds new books to the books section one-by-one
        bookHolder = dataOut['books']
        for boo in dataIn:
            bookHolder.append(boo)
        #store the sum of old & new info in dataOut
        dataOut = {'metadata': metaIn, 'books': bookHolder}
        
    else:
        #ie if this is the first retrieval
        dataOut = {'metadata': metaIn, 'books': dataIn}
    
    #write to the file
    # file = open('static/data/data.json','w')
    file = 'static/data/data.json'
    with open(file, 'w') as data_file:
        json.dump(dataOut, data_file, indent = 4)

'''to be called when the website first opens; gets first 30 books' details to dump to JSON''' 
def first_retrieval():
    #storage vars for metadata and book details to go into the JSON
    bookDets = [""] * 30
    metaOut = {'genresTotal' : []}

    #retrieves the links
    f = open('static/data/links.json')
    data = json.load(f)
    f.close()
    info = data['links']
    ind = data['pointer']

    #get the book details
    while ind < 30:
        bookDets[ind] = get_book(info[ind])
        #check check if we already have the genres listed
        #if not, add the genre to the metadata
        for gen in bookDets[ind]['genres']:
            if gen not in metaOut['genresTotal']:
                metaOut['genresTotal'].append(gen)
        ind += 1
    
    #write the data to the JSON
    dumpToJSON(bookDets, metaOut)
    
    #rewrites with pointer
    file = open('static/data/links.json','w')
    json.dump({"pointer": ind, "links": info}, file, indent = 4)

    return ind

'''called upon click of button to load more;
   retrieves 30 more books' details '''
def retrieve_more():
    #retrieve links & pointer for location in book scraping
    f = 'static/data/links.json'
    with open(f, 'r') as link_file:
        data = json.load(link_file)
    info = data['links']
    ind = data['pointer']

    #open the data file to recieve the list of genres thus far
    f = 'static/data/data.json'
    with open(f, 'r') as book_data:
        fData = json.load(book_data)
    metaOut = fData['metadata']

    #stop when we're at 30 books more
    endInd = ind + 30

    #is json num entries is >= 150
    #we've got all the data
    if ind >= 150:
        return
    
    #helper var to store retrieved data
    bookDets = [""] * 30
    i = 0
    while ind < endInd:
        bookDets[i] = get_book(info[ind])
        for gen in bookDets[i]['genres']:
            if gen not in metaOut['genresTotal']:
                metaOut['genresTotal'].append(gen)
        ind += 1
        i += 1
    
    #add info to JSON file
    dumpToJSON(bookDets, metaOut)

    #update the pointer in links
    file = 'static/data/links.json'
    with open(file, 'w') as link_file:
        json.dump({"pointer": ind, "links": info}, link_file, indent = 4)

    return ind