from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') # Gets you to homepage
def home():
    return render_template('index.html')

@app.route('/search') # Searches term from form
def search():
    query = request.args.get('query')
    return query

@app.route('/results/<query>')
def display_results(query):
    return render_template('results.html', query = query)

if __name__ == "__main__":
    app.run(debug=True)