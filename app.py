from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search
import json


app = Flask(__name__, static_url_path='/static')

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/tfidf') # Perform TF/IDF search and load results
def search():
    query = request.args.get('tf-idf-query')
    print(query)
    results = site_search(query)

    return render_template('results.html', query = query, results = results)

    #TODO: load additional results

@app.route('/book/<id>') # Show particular book
def display_book(id):
    # Open books json file
    with open('./data/data.json','r') as f:
        books = json.load(f)
    # Convert id from url to int (don't ask me how long it took me to figure out it was actually a string)
    id = int(id)
    # Grab book with matching ID from database and pass to render_template
    book = next((book for book in books if book['id'] == id), 'None')
    return render_template('book.html', book = book)

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    