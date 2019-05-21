with open("./Pymaker/datas/pythonDocToNumber.txt", 'r') as f:
    data = f.read()
    links = eval(data)
    print(links["library/functions.html#abs"])

with open("./Pymaker/datas/numberToPythonDoc.txt", 'r') as f:
    data = f.read()
    backlinks = eval(data)
    print(backlinks[303])
