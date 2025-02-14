# Libraries import
import os
import pke
import pandas as pd
import numpy as np
from collections import defaultdict

# For computing embeddings
from sentence_transformers import SentenceTransformer

# For clustering, similarity, and visualization
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

import matplotlib.pyplot as plt
import seaborn as sns

import json

with open('./data/data.json','r') as f:
    books = json.load(f)




book_reviews = [book['review'] for book in books]

def get_book_themes(book, num = 5):
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(book, language = 'en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=num)
    # print("Extracted themes:")
    # print("=================")
    # for keyphrase in keyphrases:
    #     print(f'{keyphrase[1]:.5f}   {keyphrase[0]}')
    return keyphrases


# get_book_themes(books[0]['review'])

books_slice = book_reviews[:5]

all_book_themes = [get_book_themes(book) for book in books_slice]

model = SentenceTransformer('all-MiniLM-L6-v2')
book = books_slice[0]
topics = get_book_themes(book)

weights = [t[1] for t in topics]
phrases =[t[0] for t in topics]
topics_embedding = model.encode(phrases)
topics_embedding.shape, weights
#Step 2 - Weight
weighted_topics_embedding = np.array([ topics_embedding[i]*weights[i] for i in range(len(weights))])
#Step 3 - Aggregate
document_embedding = np.mean(weighted_topics_embedding, axis=0)
weighted_topics_embedding.shape, document_embedding.shape

document_embeddings = []

for book_themes in all_book_themes:
    # doc_topics is a list of (keyphrase_string, score)
    phrases = [t[0] for t in book_themes]
    scores = np.array([t[1] for t in book_themes])

    # Encode each keyphrase
    phrase_embeddings = model.encode(phrases)

    # Weight the embeddings by their scores
    scores = scores.reshape(-1, 1)
    weighted_embeddings = phrase_embeddings * scores

    # Aggregate (mean) to get a single vector per document
    doc_embedding = np.mean(weighted_embeddings, axis=0)

    document_embeddings.append(doc_embedding)

print("Number of document embeddings:", len(document_embeddings))
print("Dimension of each embedding:", len(document_embeddings[0]))

similarities = cosine_similarity(document_embeddings)

plt.imshow(similarities, cmap='viridis', vmin=0, vmax=1)


plt.colorbar() # Add a colorbar (legend)

# Create labels for each document (Doc0, Doc1, ...)
num_docs = similarities.shape[0]
fig_labels = [f"Doc{i+1}" for i in range(num_docs)]

# Use the labels on the x-axis and y-axis
plt.xticks(np.arange(num_docs), fig_labels)
plt.yticks(np.arange(num_docs), fig_labels)


plt.title("Document Similarities") # Add a title

# Overlay the numeric values on each cell
for i in range(num_docs):
    for j in range(num_docs):
        # Format values with two decimals
        plt.text(j, i, f"{similarities[i, j]:.2f}",
                 ha='center', va='center', color='white')

plt.tight_layout()
plt.grid(False)
plt.show()