from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import json

def load_data(filepath="static/data/data.json"):
    """Loads and extracts titles and first paragraphs from the data."""
    
    with open(filepath,'r') as f:
        data = json.load(f)

    data = data['books']
    data = [item for item in data if isinstance(item, dict) and item]
    df = pd.DataFrame(data)
    df['text'] = df['review']
    return df

def clean_text(df):
    """Removes stopwords from the text column."""
    stopwordsList = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    df["text"] = df["text"].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(str(x)) 
                                                      if word.isalpha() and word not in stopwordsList]))
    return df

def vectorize_data(df):
    """Converts text into TF-IDF vectors using the same vectorizer for title and text."""
    vectorizer = TfidfVectorizer()
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["genres"].astype(str) + " " + df["text"].astype(str) 
    tfidfMatrix = vectorizer.fit_transform(combined)
    
    return vectorizer, tfidfMatrix

def search_query(query, df, vectorizer, tfidfMatrix):
    """Searches articles and prints the results."""
    queryVec = vectorizer.transform([query])
    results = cosine_similarity(tfidfMatrix, queryVec).reshape((-1,))
    
    # Find exact title matches
    exactMatches = df.loc[df[["title", "author"]].apply(lambda x: query.lower() in x.str.lower().values, axis=1)]
    if not exactMatches.empty:
        matchingIndices = exactMatches.index.to_numpy() # extract match indices as a numpy array
        sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]] # sort indices by cosine similarity 
        return sortedIndices
        
    # Find closest matches
    matchingIndices = np.where(results > 0.0)[0]  
    sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]]

    if len(sortedIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return
    
    return sortedIndices