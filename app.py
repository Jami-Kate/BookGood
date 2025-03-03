from flask import Flask, render_template, redirect, request, url_for
import json
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

        # Delete old json files
        # if os.path.exists("static/data/links.json"):
        #   os.remove("static/data/links.json")
        #if os.path.exists("static/data/data.json"): # commented this out for now because the search engine breaks otherwise ; FIX LATER
        #    os.remove("static/data/data.json")

        t = Thread(target = load_json) # Silos loading of data.json into its own thread so the rest of the app can load; @TODO: create another thread for moods
        t.start()
    else:
        print(f'{book_status} books loaded; {mood_status} moods loaded')

@app.route('/') # Gets you to homepage
def home():
    msg = request.args.get('msg')
    return render_template('index.html', msg = msg)

@app.route('/search')  # Perform search and load results
def search():
    
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

    if not os.path.exists("static/data/data.json"):
        msg = 'give me a second'
        return redirect(url_for('home', msg=msg))

    if not sortedIndices:  # Check if the array is empty
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
    print(id) 
    print(book)
    # Runs get_mood on a book if its mood hasn't already been filled in
    if book['mood'] == None:
        book['mood'] = get_mood(book['review'])

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

@app.errorhandler(404)
def err(e):
    return render_template('err.html', e = e)

if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    
