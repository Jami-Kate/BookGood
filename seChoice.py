options = {"1": "searchEngine.py", "2": "tfidfSearchEngine.py"}

while True:
    seChoice = input("What search engine would you like to use today?\n 1. Boolean\n 2. Tf-idf\n 3. Actually, I'd rather not\n")
    
    if seChoice in options:
        with open(options[seChoice]) as file:
            exec(file.read())
    elif seChoice == "3":
        print("See you later!")
        break
    else:
        print("Please only type 1, 2, or 3 as your answer")