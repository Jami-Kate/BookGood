from flask import Flask, render_template, request
from engine.tfidfSearchEngine import site_search, df
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import io
import base64 
from engine.bookMood import plot_moods
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
    genres = [df.iloc[idx]["genres"] for idx in sortedIndices]
    
    # Create the pie chart  
    flatGenres = []  
    for row in genres:
        flatGenres.extend(row) # merge all lists in one 
    count_ = Counter(flatGenres) # count the number of genres 
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(count_.values(), labels=count_.keys(), startangle = 90, colors=sns.color_palette('Set2'))
    
    # Convert the pie chart to an image
    img = io.BytesIO() 
    plt.savefig(img, format="png") # temporarily store the image in byte stream 
    img.seek(0)
    plt.close(fig)  # close to free memory
    img64 = base64.b64encode(img.getvalue()).decode('utf-8') # encode the imagine in base64; allows it to be enbedded in HTML without creating a separate file for it
    
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
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

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

@app.errorhandler(404)
def redirect(e):
    return render_template('err.html', e = e)


if __name__ == "__main__":
    print('watching. waiting')
    app.run(debug=True)
    