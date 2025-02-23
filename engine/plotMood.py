import matplotlib.pyplot as plt
import io

from math import pi

def plot_moods(book):
    N = len(book)
    labels = list(book.keys())
    scores = list(book.values())

    # Hacky stuff to make a circular graph work
    scores += scores[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Create radar plot
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], labels, color='grey', size=10)

    ax.set_rlabel_position(0)

    plt.yticks(color="grey", size=7)
    
    plt.ylim(0,max(scores))

    ax.plot(angles, scores, linewidth=1, linestyle='solid')

    ax.fill(angles, scores, 'b', alpha=0.1)

    img = io.BytesIO()
    return ax, img