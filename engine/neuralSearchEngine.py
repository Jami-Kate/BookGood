from sentence_transformers import SentenceTransformer, util
import torch
from nltk.stem import WordNetLemmatizer
from tfidfSearchEngine import clean_text, load_data
import numpy as np



corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]

model = SentenceTransformer("all-MiniLM-L6-v2")
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
corpus_embeddings.shape

queries = [
    "A man is eating pasta.",
    "Someone in a gorilla costume is playing a set of drums.",
    "A cheetah chases prey on across a field.",
]

for query in queries:
    query_embedding = model.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 3 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    most_similar = torch.topk(cos_scores, k=3)
    print("Query:", query)
    for score, idx in zip(most_similar[0], most_similar[1]):
        print(f"- {corpus[idx]} (Score: {score:.4f})")
    print()