from sklearn.feature_extraction.text import CountVectorizer
from err import handle_errors
import re
    
### GETTING AND ORGANIZING DATA ###
         
data = open("wikiData.txt", "r", encoding="utf8")
#begin the documents array to store the articles
documents2 = [""]
i = 0

for line in data:
    #print all lines except the article tags
    if line != "</article>\n":
        documents2[i] = documents2[i] + line
    else:
        i = i + 1
        documents2.append("")

titles = []
paragraphs = []

for document in documents2:
    matches = re.findall(r'<article name="(.*?)">\n(.*?)\n', document) #divide the document into articles 
    for match in matches:
        titles.append(match[0])  # Title
        paragraphs.append(match[1])  # First paragraph

# FOR TESTING #
#print(titles) #a list of titles
#print(len(paragraphs)) #number of paragraphs (should match the number of titles)
#print(len(titles)) #number of titles
#print(paragraphs[0]) #prints out first paragraph 

### VECTORIZER STARTS HERE ### 
    
cv = CountVectorizer(lowercase=True, binary=True)

sparse_matrix = cv.fit_transform(documents2)
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
    for doc_idx in hits_list:
        print("Matching doc:", titles[doc_idx], "\n", paragraphs[doc_idx])
        print()

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

### USER INPUT STARTS HERE ###

usr_input = input("What are we searching for today? Enter your query or leave the field blank to quit ")

while usr_input:
    try:
        print(test_query(usr_input.lower()))
    except:
        print(f"Uh oh!") # This'll prevent the engine from crashing but it's not desperately sophisticated
        all_terms = usr_input.split()
        problem_terms = []
        prev = ''
        for term in all_terms:
            if term not in list(d.keys()):
                try:
                    if prev.lower() == 'not':

                        term = prev + " " + term
                    print(f"trying {term}")
                    print(eval(rewrite_query(term)))
                except:
                    problem_terms.append(term)
            prev = term
        if problem_terms:
            print(f"Nothing found for {problem_terms}, I'm afraid")

    usr_input = input("Anything else? Enter another query or leave the field blank to quit ")
print("See you later")

