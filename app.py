from flask import Flask, render_template, flash, redirect, request, url_for
import json
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from engine.getMood import get_mood, next_mood_batch, first_mood_batch
from engine.bookRetrieval import *
from engine.tfidfSearchEngine import load_data, clean_text, vectorize_data, search_query
from threading import Thread

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
        if os.path.exists("static/data/links.json"):
            os.remove("static/data/links.json")
        if os.path.exists("static/data/data.json"):
            os.remove("static/data/data.json")

        t = Thread(target = load_json) # Silos loading of data.json into its own thread so the rest of the app can load; @TODO: create another thread for moods
        t.start()
    else:
        print(f'{book_status} books loaded; {mood_status} moods loaded')

@app.route('/') # Gets you to homepage
def home():
    msg = request.args.get('msg')
    return render_template('index.html', msg = msg)

@app.route('/tfidf') # Perform TF/IDF search and load results
def search():
    query = request.args.get('tf-idf-query')
    if not query:
        msg = 'cmon you gotta enter something'
        return redirect(url_for('home', msg = msg))
    print(query)
    df = load_data()
    df = clean_text(df)
    vectorizer, tfidfMatrix = vectorize_data(df)
    sortedIndices = search_query(query, df, vectorizer, tfidfMatrix)
    try:
        results = [df.iloc[idx] for idx in sortedIndices]
        fig, genrePie = plot_pie(df, sortedIndices)
        img64 = create_image(fig, genrePie)
    except:
        msg = f'weh woh nothing found for {query}'
        return redirect(url_for('home', msg = msg))
    return render_template('results.html', query = query, results = results, plot = img64)

@app.route('/book/<id>') # Show particular book
def display_book(id):
    # Open books json file
    with open('static/data/data.json','r') as f:
        books = json.load(f)
        books = books['books']
    # Convert id from url to int (don't ask me how long it took me to figure out it was actually a string)
    id = int(id)
    # Grab book with matching ID from database and pass to render_template
    book = next((book for book in books if book['id'] == id), 'None')    

    # Runs get_mood on a book if its mood hasn't already been filled in
    if 'mood' not in book.keys():
        book['mood'] = get_mood(book['review'])

    mood_fig, mood_img = plot_moods(book['mood'])
    mood64 = create_image(mood_fig, mood_img)

    return render_template('book.html', book = book, mood = mood64)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route("/genres/<genre>")
def display_genres(genre):
    with open('./data/data.json','r') as f:
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
    
