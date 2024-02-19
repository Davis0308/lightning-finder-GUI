import validators


while True:
    link = input()
    print(validators.url(link))