from flask import Flask, render_template, flash, redirect, request, url_for
import json
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from engine.getMood import get_mood
from engine.bookRetrieval import *
from engine.tfidfSearchEngine import load_data, clean_text, vectorize_data, search_query

app = Flask(__name__, static_url_path='/static')

starting_up = True

@app.before_request
def load_json():
    global starting_up
    if starting_up:
        print('fetching links')
        book_links()
        print('loading json')
        ind = first_retrieval()
        while ind: 
            ind = retrieve_more()
            print(f'retrieved {ind}')

        with open('static/data/data.json','r') as f:
            books = json.load(f)
            books = books['books']
        print(f'length: {len(books)}')

        starting_up = False
    else:
        print('json already loaded')


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
    print(book)
   
    mood = get_mood(book['review'])
    mood_fig, mood_img = plot_moods(mood)
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

@app.errorhandler(404)
def err(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    
