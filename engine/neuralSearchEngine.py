import pandas as pd
import numpy as np
import json
import torch.nn.functional as F
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

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


def get_sentence_embeddings(sentences, model):
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True) 
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1) # normalize embeddings 
    return sentence_embeddings

def compute_similarities(emb1, emb2):
    return [cosine_similarity(x.cpu().numpy().reshape(1, -1), 
                              y.cpu().numpy().reshape(1, -1))[0][0] 
            for x, y in zip(emb1, emb2)]


def vectorize_data(df):
    """Computes sentence embeddings for each text in the dataset."""
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    combined = df["author"].astype(str) + " " + df["title"].astype(str) + " " + df["genres"].astype(str) + " " + df["text"].astype(str) 
    embeddings = get_sentence_embeddings(combined.tolist(), model)  # Convert to tensor
    
    return model, embeddings

def neural_search(query, model, embeddings, df):
    """Searches for the most relevant books based on the query."""
    query_embedding = get_sentence_embeddings([query], model)  # Encode query
    similarities = cosine_similarity(query_embedding.cpu().numpy(), embeddings.cpu().numpy()).flatten()

    sorted_indices = np.argsort(similarities)[::-1]  # Sort in descending order
    return sorted_indices

# df = load_data()
# df = clean_text(df)
# model, neuralMatrix = vectorize_data(df)

# def query_search(query):
#     return neural_search(query, model, neuralMatrix, df)
