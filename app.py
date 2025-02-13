from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search


app = Flask(__name__, static_url_path='/static')

@app.route('/') # Gets you to homepage
def home():
    print('come on man')
    return render_template('index.html')

@app.route('/tfidf') # Just pukes out everything in data.json right now! But just you wait
def search():
# Open and read JSON file
    query = request.args.get('tf-idf-query')
    print(query)
    results = site_search(query)

    # Renders results template; passes in query and results
    return render_template('results.html', query = query, results = results)

    # Call retreive_books (gets 150 books)
    # Display first 30 results
    # Get 30

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    