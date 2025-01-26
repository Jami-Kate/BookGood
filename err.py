d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def list_problem_terms(problem_terms):
    print("I'm afraid we've found no results for the following:")
    for problem_term in problem_terms:
        print(f"---{problem_term}")

def handle_errors(search, terms):
    try:
        search(terms)
    except:
        print(f"There's a problem with your query '{terms}'!")
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
