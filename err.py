from config import d

# Processes the input by putting it in lowercase, then adds a space after an open-paren and before a close-paren
def process_input(input):
    return input.lower().replace("(", "( ").replace(")", " )")

# Lists all search terms for which there is no result
def list_problem_terms(problem_terms):
    print("I'm afraid we've found no results for the following:")
    for problem_term in problem_terms:
        print(f"---{problem_term}")

# Tries the search query. If unsuccessful, attempts to break query into chunks and search each chunk individually
def handle_errors(search, terms):
    try:
        search(process_input(terms))
    except:
        print(f"Uh oh, there's a problem with your query!")
        all_terms = terms.split()
        problem_terms = []
        prev = ''
        if len(all_terms) > 1:
            for term in all_terms:
                if term not in list(d.keys()):
                    try:
                        if prev.lower() == 'not':
                            term = prev + " " + term
                        print(f"Let's try searching for {term}")
                        search(term)
                    except:
                        problem_terms.append(term)
                prev = term
        else: problem_terms.append(terms)
        list_problem_terms(problem_terms)

print(process_input("Let's process (a (test sentence) with (parens))"))