from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import json

def load_data(filepath="./data/data.json"):
    """Loads and extracts titles and first paragraphs from the data."""
    
    with open(filepath,'r') as f:
        data = json.load(f)

    data = [item for item in data if isinstance(item, dict) and item]
    df = pd.DataFrame(data)
    df['text'] = df['review']
    return df

def clean_text(df):
    """Removes stopwords from the text column."""
    stopwordsList = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    df["text"] = df["text"].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(str(x)) 
                                                      if word.isalpha() and word not in stopwordsList]))
    return df

def vectorize_data(df):
    """Converts text into TF-IDF vectors using the same vectorizer for title and text."""
    vectorizer = TfidfVectorizer()
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["text"].astype(str)  # Merge author, title and text
    tfidfMatrix = vectorizer.fit_transform(combined)
    
    return vectorizer, tfidfMatrix

def search_query(query, df, vectorizer, tfidfMatrix):
    """Searches articles and prints the results."""
    queryVec = vectorizer.transform([query])
    results = cosine_similarity(tfidfMatrix, queryVec).reshape((-1,))
    
    # Find exact title matches
    exactMatches = df.loc[df[['title', 'author']].apply(lambda x: query.lower() in x.str.lower().values, axis=1)]
    if not exactMatches.empty:
        print(f"\nExact match found for '{query}':\n")
        for _, row in exactMatches.iterrows(): # _, to ignore indices 
            print(f"Title: {row['title']}")
            print(f"Author: {row.get('author')}")
            print(f"Description: {row['review']}")
            print("-" * 80)
        return
    
    # Find closest matches
    matchingIndices = np.where(results > 0.0)[0]
    sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]]

    if len(sortedIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return

    print(f"\nResults for '{query}':\n")
    for idx in sortedIndices[:5]:  # Limit results to top 5
        title = df.iloc[idx]["title"]
        author = df.iloc[idx].get("author")
        text = df.iloc[idx]["review"]
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Description: {text}")
        print(f"Similarity Score: {results[idx]:.4f}")
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