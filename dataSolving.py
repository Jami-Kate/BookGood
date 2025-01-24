data = open("wikiData.txt", "r")
#begin the documents array to store the articles
documents = [""]
i = 0

for line in data:
    #print all lines except the article tags
    if line != "</article>\n":
        documents[i] = documents[i] + line
    else:
        i = i + 1
        documents.append("")

