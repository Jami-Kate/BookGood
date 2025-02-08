from flask import Flask, render_template, request
from engine.bookRetrieval import book_links

app = Flask(__name__)

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/search') # Just returns your search query rn! But just you wait
def search():
    book_links()
    query = request.args.get('query')
    return render_template('results.html', query = query, results = [query, query, query])

    # Call retreive_books (gets 150 books)
    # Display first 30 results
    # Get 30



if __name__ == "__main__":
    app.run(debug=True)