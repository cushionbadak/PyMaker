import json

with open("./Pymaker/datas/pythonDocListLibraryReference.txt", 'r') as f:
    data = f.read()
    data = data.replace("'", '\"')
    links = json.loads(data)
    print(links["library/functions.html#abs"])