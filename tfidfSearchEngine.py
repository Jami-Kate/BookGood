from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re
import requests

def load_data(file_path="wikiData.txt"):
    """Loads and extracts titles and first paragraphs from the data."""
    
    documents = [""]
    i = 0
    
    with open(file_path, "r", encoding="utf8") as data:
        for line in data:
            if line != "</article>\n":
                documents[i] += line
            else:
                i += 1
                documents.append("")

    titles = []
    paragraphs = []
    for document in documents:
        matches = re.findall(r'<article name="(.*?)">\n(.*?)\n', document)
        for match in matches:
            titles.append(match[0])  
            paragraphs.append(match[1])  

    df = pd.DataFrame({"title": titles, "text": paragraphs})
    return df

def clean_text(df):
    """Removes stopwords from the text column."""
    stopwordsList = requests.get(
        "https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt"
    ).content
    stopwords = set(stopwordsList.decode().splitlines())

    df["text"] = df["text"].apply(lambda x: [word for word in str(x).split() if word.lower() not in stopwords])
    return df

def vectorize_data(df):
    """Converts text into TF-IDF vectors."""
    vectorizer = TfidfVectorizer()
    tfidfMatrix = vectorizer.fit_transform(df["text"])
    return vectorizer, tfidfMatrix

def search_query(query, df, vectorizer, tfidfMatrix):
    """Searches articles and prints the results."""
    queryVec = vectorizer.transform([query])
    results = cosine_similarity(tfidfMatrix, queryVec).reshape((-1,)) 

    matchingIndices = np.where(results > 0.0)[0] # selecting results that are higher than 0.0
    sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]] # retrieve highest values from the array
    if len(sortedIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return

    print(f"\nQuery: '{query}'\n")
    for idx in sortedIndices:
        title = df.iloc[idx]["title"] 
        text = df.iloc[idx]["text"]
        print(f"Title: {title}")
        print(f"First paragraph: {text}") 
        print(f"Similarity Score: {results[idx]:.4f}") # added this mainly to make sure the result with the highest score is at the top 
        print("-" * 80)

def user_search(df, vectorizer, tfidfMatrix):
    """Asks for user input until the user quits."""
    
    query = input("What are we searching for today? Enter your query or leave the field blank to quit:\n")
    while query:
        search_query(query, df, vectorizer, tfidfMatrix)
        query = input("Anything else? Enter another query or leave the field blank to quit:\n")
    print("See you later!")

df = load_data()
df = clean_text(df)
vectorizer, tfidfMatrix = vectorize_data(df)
user_search(df, vectorizer, tfidfMatrix)
