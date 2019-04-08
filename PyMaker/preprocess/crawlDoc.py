import requests
from bs4 import BeautifulSoup as bs
import json

response = requests.get("https://docs.python.org/3/contents.html")
html = response.content
contents = bs(html, "html.parser")

links = {}
cnt = 0

for refer in contents.find_all('a', {"class" : "reference internal"}):
    href = refer["href"]
    if (("library" in href) == True or ("reference" in href) == True) and ('#' in href) == False and links.get(href) == None:
        links[href] = cnt
        cnt += 1

        response = requests.get("https://docs.python.org/3/" + href)
        html = response.content
        doc = bs(html, "html.parser")
        
        for header in doc.find_all('a', {"class" : "headerlink"}):
            link = header["href"]
            if ('#' in link) == True and links.get(href + link) == None:
                links[href + link] = cnt
                cnt += 1

with open("./Pymaker/datas/pythonDocListLibraryReference.txt", 'w') as f:
    f.write(str(links))
