from sklearn.feature_extraction.text import CountVectorizer

documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)

print("Term-document matrix: (?)\n")
print(sparse_matrix)

dense_matrix = sparse_matrix.todense()

print("Term-document matrix: (?)\n")
print(dense_matrix)

td_matrix = dense_matrix.T   # .T transposes the matrix

print("Term-document matrix:\n")
print(td_matrix)

print("\nIDX -> terms mapping:\n")
print(cv.get_feature_names_out())

terms = cv.get_feature_names_out()

print("First term (with row index 0):", terms[0])
print("Third term (with row index 2):", terms[2])

print("\nterm -> IDX mapping:\n")
print(cv.vocabulary_) # note the _ at the end

print("Row index of 'example':", cv.vocabulary_["example"])
print("Row index of 'silly':", cv.vocabulary_["silly"])

t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
print("Query: example")
print(td_matrix[t2i["example"]])

print("Query: example AND great")
print("example occurs in:                            ", td_matrix[t2i["example"]])
print("great occurs in:                              ", td_matrix[t2i["great"]])
print("Both occur in the intersection (AND operator):", td_matrix[t2i["example"]] & td_matrix[t2i["great"]])

print("Query: is OR see")
print("is occurs in:                            ", td_matrix[t2i["is"]])
print("see occurs in:                           ", td_matrix[t2i["see"]])
print("Either occurs in the union (OR operator):", td_matrix[t2i["is"]] | td_matrix[t2i["see"]])

print("Query: NOT this")
print("this occurs in:                     ", td_matrix[t2i["this"]])
print("this does not occur in (complement):", 1 - td_matrix[t2i["this"]]) # 1 - x changes 1 to 0 and 0 to 1

print("Query: ( example AND NOT this ) OR nothing")
print("example occurs in:                  ", td_matrix[t2i["example"]])
print("this does not occur in:             ", 1 - td_matrix[t2i["this"]])
print("example AND NOT this:               ", td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]]))
print("nothing occurs in:                  ", td_matrix[t2i["nothing"]])
print("( example AND NOT this ) OR nothing:", 
      (td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]])) | td_matrix[t2i["nothing"]])

# Operators and/AND, or/OR, not/NOT become &, |, 1 -
# Parentheses are left untouched
# Everything else is interpreted as a term and fed through td_matrix[t2i["..."]]

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    print()

test_query("example AND NOT nothing")
test_query("NOT example OR great")
test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
test_query("( not example or great ) and nothing") # ... or all small letters
test_query("not example and not nothing")

print(sparse_matrix)

print(sparse_matrix.tocsc())

print(sparse_matrix.T)

sparse_td_matrix = sparse_matrix.T.tocsr()
print(sparse_td_matrix)

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

test_query("NOT example OR great")

hits_matrix = eval(rewrite_query("NOT example OR great"))
print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
print("The coordinates of the non-zero elements:", hits_matrix.nonzero()) 

hits_list = list(hits_matrix.nonzero()[1])
print(hits_list)

for doc_idx in hits_list:
    print("Matching doc:", documents[doc_idx])

for i, doc_idx in enumerate(hits_list):
    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))


usr_input = input("What are we searching for today? Enter your query or leave the field blank to quit ")

while usr_input:
    try:
        test_query(usr_input)
    except:
        print(f"No results for {usr_input}!")
    usr_input = input("Anything else? Enter another query or leave the field blank to quit ")
print("See you later")