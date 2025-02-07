from bookRetrieval import *

#run upon loading between *
# *
t = LMnger()
t.links = book_links()
bookDets = [""] * (len(t.links))
t.details = first_retrieval(t.links,bookDets)
# *


ind = 1

# between the * run each time the 'load more' button runs
# *
t.details = retrieve_more(t.links,t.details,ind)

ind += 1
# *