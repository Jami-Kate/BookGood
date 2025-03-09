from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Dictionary for operator replacements
OPERATOR_REPLACEMENTS = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

def preprocess_query(query):
    """Replace natural language operators with symbolic representations."""
    # Split the query into tokens (words and operators)
    tokens = re.findall(r'\b\w+\b|\(|\)', query)
    
    # Replace operators using the dictionary
    processed_tokens = [OPERATOR_REPLACEMENTS.get(token, token) for token in tokens]
    
    # Join the tokens back into a single query string
    processed_query = ' '.join(processed_tokens)
    return processed_query

def vectorize_data(df):
    """Creates a Boolean term-document matrix."""
    vectorizer = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b') 
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["genres"].astype(str) + " " + df["text"].astype(str) 
    booleanMatrix = vectorizer.fit_transform(combined)
    
    return vectorizer, booleanMatrix

def query_search(query, vectorizer, booleanMatrix):
    """Search using Boolean logic."""
    # Preprocess the query to replace operators
    processed_query = preprocess_query(query)
    print(f"Processed query: {processed_query}")  # Debug statement
    
    # Transform the processed query into a vector
    queryVec = vectorizer.transform([processed_query])
    
    # Calculate cosine similarity between the query and documents
    matches = cosine_similarity(booleanMatrix, queryVec).flatten()    
    
    # Find indices of documents with a match (cosine similarity > 0)
    matchingIndices = np.where(matches > 0)[0] 

    if len(matchingIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return []

    return matchingIndices