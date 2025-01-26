def handle_errors(func):
    try:
        print(func())
    except:
        print('wuh woh')