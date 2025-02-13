from flask import Flask, render_template, request
from engine.bookRetrieval import *


app = Flask(__name__)

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/search') # Just pukes out everything in data.json right now! But just you wait
def search():
# Open and read JSON file
    with open('data/data.json', 'r') as file:
        data = json.load(file)
    
    #TODO: apply query to data
    query = request.args.get('query')
    results = data

    # Renders results template; passes in query and results
    return render_template('results.html', query = query, results = results)

    # Call retreive_books (gets 150 books)
    # Display first 30 results
    # Get 30

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    app.run(debug=True)