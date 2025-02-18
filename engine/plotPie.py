from collections import Counter
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io 

# Create the pie chart  
def plot_pie(df, sortedIndices):

    genres = [df.iloc[idx]["genres"] for idx in sortedIndices]
    flatGenres = []  
    for row in genres:
        flatGenres.extend(row) # merge all lists in one 
    count_ = Counter(flatGenres) # count the number of genres 
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(count_.values(), labels=count_.keys(), startangle = 90, colors=sns.color_palette('Set2'))
    img = io.BytesIO()
    
    return fig, img 