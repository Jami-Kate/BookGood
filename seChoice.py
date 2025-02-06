seChoice = input("What search engine would you like to use today?\n 1. Boolean\n 2. Tf-idf\n 3. Actually, I'd rather not\n")

if seChoice == "1":
    filename = 'searchEngine.py'
    with open(filename) as file:
        exec(file.read())
elif seChoice == "2":
    filename = 'tfidfSearchEngine.py'
    with open(filename) as file:
        exec(file.read())
elif seChoice == "3": 
    print("See you later!")
else:
    print("Please only type 1, 2, 3 as your answer")