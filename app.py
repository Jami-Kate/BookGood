from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search


app = Flask(__name__, static_url_path='/static')

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/tfidf')
def search():
    query = request.args.get('tf-idf-query')
    print(query)
    results = site_search(query)

    return render_template('results.html', query = query, results = results)

    #TODO: load additional results

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    