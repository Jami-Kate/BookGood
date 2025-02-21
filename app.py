from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search, df
import json
from engine.plotMood import plot_moods
from engine.createImage import create_image
from engine.plotPie import plot_pie
from transformers import pipeline

app = Flask(__name__, static_url_path='/static')

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/tfidf') # Perform TF/IDF search and load results
def search():
    query = request.args.get('tf-idf-query')
    print(query)
    sortedIndices = site_search(query)
    results = [df.iloc[idx] for idx in sortedIndices]
    fig, genrePie = plot_pie(df, sortedIndices)
    img64 = create_image(fig, genrePie)
    
    return render_template('results.html', query = query, results = results, plot = img64)

    #TODO: load additional results

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

    # Grab roberta classifier
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", max_length = 512, top_k=None)
    
    #TODO: chunk reviews
    # Run classifier on review of book and generate plot of its top five moods
    model_outputs = classifier(book['review'])[0]
    mood_fig, mood_img = plot_moods(model_outputs)
    mood64 = create_image(mood_fig, mood_img)
    return render_template('book.html', book = book, mood = mood64)

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    
