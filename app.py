from flask import Flask, render_template, redirect, request, url_for, abort
import json
import os
from random import choice
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from engine.getMood import get_mood, next_mood_batch, first_mood_batch
from engine.bookRetrieval import *
from engine.tfidfSearchEngine import correct_query, vectorize_data as tfidf_vectorize, search_query as tfidf_search
from engine.booleanSearchEngine import vectorize_data as b_vectorize, query_search as b_search
from engine.neuralSearchEngine import vectorize_data as n_vectorize, neural_search as n_search
from engine.searchHelpers import load_data, clean_text
from threading import Thread
from time import sleep

app = Flask(__name__, static_url_path='/static')

starting_up = True # Make sure data.json is only refreshed when the app starts up

# Keep track of how many books/moods have been loaded
book_status = 0
mood_status = 0

def load_json():
    global book_status
    global mood_status
    print('fetching links')
    book_links() # Grab book links
    print('loading books')
    book_status = first_retrieval() # Retrieve first 30 books and set book_status to 30
    while book_status: 
        book_status = retrieve_more() # Retrieve books in chunks of 30 until 150 is reached
    book_status = 150 # Set status to 150 and stop retrieving
    print('books loaded')
    # Same deal with moods
    mood_status = first_mood_batch() 
    while mood_status:
        mood_status = next_mood_batch(mood_status)
    mood_status = 150
    print('moods loaded')
    

# Runs before every API request to see if it needs to load data.json (i.e. this is the first request)
@app.before_request
def check_data():
    global starting_up
    if starting_up:
        starting_up = False

        global book_status
        global mood_status

        # Check if data.json file exists
        if not os.path.exists("static/data/data.json"):
            print('Data file not found, loading books and moods...')
            load_json()  # Load data only if it doesn't exist
        else:
            print('Data file found, skipping loading.')

        # Check if books are loaded and process them
        with open("static/data/data.json", "r") as f:
            data = json.load(f)
            if "books" in data and len(data["books"]) >= 150:
                print("Books already loaded, skipping retrieval.")
                book_status = 150 
            else:
                print('Loading books...')
                book_status = first_retrieval()  

        while book_status: 
            book_status = retrieve_more()  
        book_status = 150  
        print('Books loaded')

        # Check if moods are loaded and process them
        if os.path.exists("static/data/data.json"):
            with open("static/data/data.json", "r") as f:
                mood_data = json.load(f)

            books = mood_data.get("books", [])
            mood_status = 0

            # Check if all books have moods
            for book in books:
                if "mood" not in book or not book["mood"]:
                    mood_status = 1  # Some books are missing moods, need to retrieve
                    break

            if mood_status == 0:  # If all books have moods, skip retrieval
                mood_status = 150
                print("Moods already loaded, skipping retrieval.")
            else:
                print("Some moods missing, starting retrieval...")
                mood_status = first_mood_batch()

                # Only run next_mood_batch if moods are missing
                while mood_status:
                    mood_status = next_mood_batch(mood_status)
                print('Moods loaded')
        else:
            print(f'{book_status} books loaded; {mood_status} moods loaded')


@app.route('/') # Gets you to homepage
def home():
    msg = request.args.get('msg')
    return render_template('index.html', msg = msg)

@app.route('/search')  # Perform search and load results
def search():

    if not os.path.exists("static/data/data.json"):
        msg = 'give me a second'
        return redirect(url_for('home', msg=msg))
    
    query = request.args.get('query', '').strip()  

    if not query:  
        msg = 'cmon you gotta enter something'
        return redirect(url_for('home', msg=msg))

    query = correct_query(query)
    search_type = request.args.get('search_type') 

    df = load_data()
    df = clean_text(df)

    if search_type == "tfidf":
        vectorizer, tfidfMatrix = tfidf_vectorize(df)
        sortedIndices = tfidf_search(query, df, vectorizer, tfidfMatrix)
        # sortedIndices = site_search(query)  # TF-IDF search function
    elif search_type == "neural":
        model, embeddings = n_vectorize(df)
        sortedIndices = n_search(query, model, embeddings, df)
        # sortedIndices = query_search(query) # neural search 
    else:
        vectorizer, booleanMatrix = b_vectorize(df)
        sortedIndices = b_search(query, vectorizer, booleanMatrix)
        # sortedIndices = boolean_search(query)  # Boolean search function

    print(f'results: {sortedIndices}')

    if len(sortedIndices) == 0:  # Check if the array is empty
        msg = f'weh woh nothing found for "{query}"'
        return redirect(url_for('home', msg=msg))

    try:
        results = [df.iloc[idx] for idx in sortedIndices]
        resultsNumber = len(results)
        fig, genrePie = plot_pie(df, sortedIndices)
        img64 = create_image(fig, genrePie)
    except:
        msg = f'weh woh something went wrong with "{query}"'
        return redirect(url_for('home', msg=msg))

    return render_template('results.html', query=query, results=results, plot=img64, resultsNumber=resultsNumber)


@app.route('/book/<id>') # Show particular book
def display_book(id):
    # Open books json file

    # Halt execution if data.json has been deleted and wait for it to come back
    while not os.path.exists("static/data/data.json"):
        sleep(.2)

    with open('static/data/data.json','r') as f:
        books = json.load(f)
    books = books['books']
    # Convert id from url to int (don't ask me how long it took me to figure out it was actually a string)
    id = int(id)
    # Grab book with matching ID from database and pass to render_template
    book = next((book for book in books if book['id'] == id), 'None')   
    # Runs get_mood on a book if its mood hasn't already been filled in
    try: # This is in case someone messes with the url directly for some god-awful reason
        if book['mood'] == None:
            book['mood'] = get_mood(book['review'])
    except:
        abort(404)

    mood_fig, mood_img = plot_moods(book['mood'])
    mood64 = create_image(mood_fig, mood_img)

    return render_template('book.html', book = book, mood = mood64)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route("/genres/<genre>")
def display_genres(genre):
    with open('static/data/data.json','r') as f:
        books = json.load(f)
        books = books['books']
    queryGenres = [book for book in books if genre in book['genres']]
    return render_template('genres.html', genre=genre, books=queryGenres)

# Gets status of book and mood retrieval to update the user in real time
@app.route('/status')
def get_status():
    statusList = {'book_status':book_status, 'mood_status':mood_status}
    return json.dumps(statusList)

@app.errorhandler(Exception)
def generic_handler(e):
    img = choice(os.listdir('static/err_pics'))
    return render_template('err.html', e = e, img = img)

if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    
