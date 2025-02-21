from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search, df
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64 
from engine.bookMood import plot_moods
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
    modelPath = "SamLowe/roberta-base-go_emotions"
    classifier = pipeline(task="text-classification", model=modelPath, tokenizer=modelPath, max_length=512, truncation=True, top_k=None)

    # Run classifier on review of book and generate plot of its top five moods
    model_outputs = classifier(book['review'])[0]
    mood_plot = plot_moods(model_outputs)

    # Convert mood plot to image (shamelessly ripping off Sonja's code here)
    img = io.BytesIO() 
    plt.savefig(img, format="png") # temporarily store the image in byte stream 
    img.seek(0)
    plt.close(mood_plot)  # close to free memory
    mood64 = base64.b64encode(img.getvalue()).decode('utf-8') # encode the imag in base64; allows it to be enbedded in HTML without creating a separate file for it

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
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    
