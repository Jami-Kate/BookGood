from sklearn.feature_extraction.text import CountVectorizer
import re
    
### GETTING AND ORGANIZING DATA ###
         
data = open("wikiData.txt", "r", encoding="utf8")
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

titles = []
paragraphs = []

for document in documents:
    matches = re.findall(r'<article name="(.*?)">\n(.*?)\n', document) #divide the document into articles 
    for match in matches:
        titles.append(match[0])  # Title
        paragraphs.append(match[1])  # First paragraph

### VECTORIZER STARTS HERE ### 
    
cv = CountVectorizer(lowercase=True, binary=True, token_pattern='(?u)\\b\\w+\\b') # changed token_pattern so that it counts all words containing alpha-numerical characters as tokens

sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T   # .T transposes the matrix
sparse_td_matrix = sparse_matrix.T.tocsr()
terms = cv.get_feature_names_out()
t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("-----"*len(query))
    print("Query: '" + query + "'")
    print("-----"*len(query))
    hits_matrix = eval(rewrite_query(query)) # Eval runs the string as a Python command
    hits_list = list(hits_matrix.nonzero()[1]) 
    
    valid_hits = [idx for idx in hits_list if idx < len(titles)] # added this to make sure the hits_list and query result indices align 
    if not valid_hits:
        print(f"No results for {query}!\n")
        return

    for doc_idx in valid_hits: 
        print("Matching doc:", titles[doc_idx], "\n", paragraphs[doc_idx])
        print()

### USER INPUT STARTS HERE ###

usr_input = input("What are we searching for today? Enter your query or leave the field blank to quit ")

while usr_input:
    try:
        test_query(usr_input.lower()) #added .lower() in case someone wants to type in all caps 
    except:
        print(f"No results for {usr_input}!") # This'll prevent the engine from crashing but it's not desperately descriptive
    usr_input = input("Anything else? Enter another query or leave the field blank to quit ")
print("See you later")