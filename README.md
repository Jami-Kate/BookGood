# BookGood
By: Jami Biddle | Edward Delmonico | Sonja Tapio

## Introduction

What if book... was good? BookGood is an app for searching and recommending books based on reviews. The user can search directly for books using BookGood's Boolean search, or for more abstract concepts like "intense" or "visceral" with tf/idf and neural search functionality. The app then displays matching results and their distribution among genres. In addition, BookGood leverages sentiment analysis tools to evaluate the most prominent "moods" of a given book.

Project for Building NLP Applications, University of Helsinki LDA-T316

## Features
* Boolean, TF/IDF, and neural search capability
* Data visualization such as distribution of search results by genre
* Sentiment analysis and visualization
* Search query spell checking
* Sorting by genre

## Installation
BookGood, in its current incarnation, is not hosted remotely, and thus requires some setup on your local machine. Never fear! We've outlined the basic procedure below.

1. **Clone the repository-** In order to install BookGood you must first, well, install BookGood. In your command line, simply navigate to the directory in which you want BookGood to live and enter ```git clone https://github.com/Jami-Kate/BookGood```

2. **Install dependencies-** Now we install all the packages BookGood needs to do its thing. 
    1. **Install pip-** BookGood uses the package manager pip to manage its dependencies, so make sure you have it! Mac and Linux users can run ```python3 -m ensurepip --default-pip``` in their command line, while Windows users can do the same with ```py get-pip.py```.
    2. **Create virtual environment-** When you're working with a Python application it's always a good idea to create a *virtual environment*, a little pocket universe in your computer for all your packages and whatnot to live in. It's as easy as running ```python -m venv venvName``` (replace "venvName" there with whatever you want your virtual environment to be called). Then, run the ```source``` command on the relative path to the "activate" file in your virtual environment folder. The full command should look something like this: ```source path/to/venvName/bin/activate ```. You'll know this has worked when you see the name of your virtual environment alongside the prompt in your command line. 
    3. **Complete the installation-** After all that setup, this step should be (we hope) pretty breezy. Simply run the command ```pip install -r requirements.txt``` and pip will install everything BookGood needs to run!

3. **Set environment variables-** Optional, but recommended! Copy and paste the following lines into the "activate" script in your virtual environment to make tinkering and running with BookGood a tad easier.
    * ```export FLASK_DEBUG=True``` lets you run BookGood interactively-- that is, it'll restart automatically every time you change something. Can't recommend it enough.
    * ```export FLASK_APP=app.py``` tells Flask to run app.py, the protagonist (if you will) of our app, by default.
    * ```export FLASK_RUN_PORT=8000``` tells Flask to listen on port 8000.

4. **Try out the app-** The moment of truth! If you completed step 3 above, all you need to do is run the command ```flask run```. 
>**Note!** The first time you start up BookGood, it's going to perform a one-time installation of the pretrained models it uses for sentiment analysis, neural search, and automatic spell-checking. Yes, there's still a little more installing to be done. We're sorry for lying to you. Fortunately, however, this requires no intervention on your part. Just grab a cup of coffee and let it run.

Once you get the message ```Running on http://127.0.0.1:8000``` in your command line, you're good to go! Head over to ```http://127.0.0.1:8000/``` or ```localhost:8000/``` and enjoy.

Book? Good.
