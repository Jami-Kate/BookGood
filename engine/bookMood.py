from transformers import pipeline

import matplotlib.pyplot as plt

# import json

from math import pi

# with open('./data/data.json','r') as f:
#     books = json.load(f)


# test_review = books[0]['review']
# print(test_review)

# # Runs classifier on selected book review to extract list of moods
# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# model_outputs = classifier(test_review)[0]
# print(model_outputs)

def plot_moods(book, n = 5):
    book = [mood for mood in book if mood['label'] != 'neutral'][:n] # Filter out the 'neutral' label if present and make a list of n most prominent moods (5 by default)
    N = len(book)
    labels = [mood['label'] for mood in book]
    scores = [mood['score'] for mood in book]

    # Hacky stuff to make a circular graph work
    scores += scores[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Create polar plot
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], list(labels), color='grey', size=10)

    ax.set_rlabel_position(0)

    plt.yticks(color="grey", size=7)
    
    plt.ylim(0,max(scores))

    ax.plot(angles, scores, linewidth=1, linestyle='solid')

    ax.fill(angles, scores, 'b', alpha=0.1)

    plt.show()

# plot_moods(model_outputs)