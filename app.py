from flask import Flask, render_template, flash, redirect, request, url_for
import json
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from engine.getMood import get_mood
from engine.bookRetrieval import *
from engine.tfidfSearchEngine import load_data, clean_text, vectorize_data, search_query
from threading import Thread

app = Flask(__name__, static_url_path='/static')

starting_up = True
book_status = 0
mood_status = 0

def load_json():
    global starting_up
    global book_status
    global mood_status
    if starting_up:
        starting_up = False
        print('fetching links')
        book_links()
        print('loading json')
        print(book_status)
        book_status = first_retrieval()
        while book_status: 
            book_status = retrieve_more()
        book_status = 150
        print('books loaded')
    else:
        print('json already loaded')

@app.route('/') # Gets you to homepage
def home():
    global book_status
    global mood_status
    t = Thread(target = load_json)
    t.start()
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
    
