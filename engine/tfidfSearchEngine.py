from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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
        matchingIndices = exactMatches.index.to_numpy() 
        sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]] 
        return sortedIndices
        
    # Find closest matches
    matchingIndices = np.where(results > 0.0)[0]  
    sortedIndices = matchingIndices[np.argsort(results[matchingIndices])[::-1]]

    if len(sortedIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return []
    
    return sortedIndices
