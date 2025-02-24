from flask import Flask, render_template, flash, redirect, request, url_for
from engine.tfidfSearchEngine import site_search, df
import json
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from engine.getMood import get_mood

app = Flask(__name__, static_url_path='/static')

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
    sortedIndices = site_search(query)
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
    with open('./data/data.json','r') as f:
        books = json.load(f)
        books = books['books']
    # Convert id from url to int (don't ask me how long it took me to figure out it was actually a string)
    id = int(id)
    # Grab book with matching ID from database and pass to render_template
    book = next((book for book in books if book['id'] == id), 'None')    
   
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
    
