from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import T5ForConditionalGeneration, AutoTokenizer
import numpy as np


def vectorize_data(df):
    """Converts text into TF-IDF vectors using the same vectorizer for title and text."""
    vectorizer = TfidfVectorizer()
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["genres"].astype(str) + " " + df["text"].astype(str) 
    tfidfMatrix = vectorizer.fit_transform(combined)
    
    return vectorizer, tfidfMatrix

def remove_repeated_words(text):
    return " ".join(dict.fromkeys(text.split()))  # keeps only first occurrence

def correct_query(query):
    if not query or not isinstance(query, str) or query.strip() == "":
        return ""  # Return an empty string instead of processing further

    modelPath = "ai-forever/T5-large-spell"
    model = T5ForConditionalGeneration.from_pretrained(modelPath)
    tokenizer = AutoTokenizer.from_pretrained(modelPath)

    encodings = tokenizer(query, return_tensors="pt", padding=True, truncation=True)

    generatedTokens = model.generate(**encodings)  
    correctedQuery = tokenizer.batch_decode(generatedTokens, skip_special_tokens=True)[0]
    cleanedQuery = remove_repeated_words(correctedQuery)

    return cleanedQuery

def search_query(query, df, vectorizer, tfidfMatrix):
    """Searches articles and prints the results."""
    query = correct_query(query)
    query = remove_repeated_words(query)  

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
