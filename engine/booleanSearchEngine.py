from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import T5ForConditionalGeneration, AutoTokenizer
import numpy as np
import pandas as pd
import json

def load_data(filepath="static/data/data.json"):
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
    """Creates a Boolean term-document matrix."""
    vectorizer = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b') 
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["genres"].astype(str) + " " + df["text"].astype(str) 
    booleanMatrix = vectorizer.fit_transform(combined)
    
    return vectorizer, booleanMatrix


def remove_repeated_words(text):
    return " ".join(dict.fromkeys(text.split()))  # keeps only first occurrence


def correct_query(query):
    modelPath = "ai-forever/T5-large-spell"
    model = T5ForConditionalGeneration.from_pretrained(modelPath)
    tokenizer = AutoTokenizer.from_pretrained(modelPath)

    encodings = tokenizer(query, return_tensors="pt")
    generatedTokens = model.generate(**encodings)  

    correctedQuery = tokenizer.batch_decode(generatedTokens, skip_special_tokens=True)[0]
    cleanedQuery = remove_repeated_words(correctedQuery)

    return cleanedQuery


def query_search(query, vectorizer, booleanMatrix):
    """Search using Boolean logic."""
    query = correct_query(query)
    query = remove_repeated_words(query)

    queryVec = vectorizer.transform([query])
    matches = cosine_similarity(booleanMatrix, queryVec).flatten()    
    matchingIndices = np.where(matches > 0)[0] 

    if len(matchingIndices) == 0:
        print(f"No matching results found for '{query}'.\n")
        return []

    return matchingIndices

# df = load_data()
# df = clean_text(df)
# vectorizer, booleanMatrix = vectorize_data(df)

# def boolean_search(query):
#     return query_search(query, vectorizer, booleanMatrix)
