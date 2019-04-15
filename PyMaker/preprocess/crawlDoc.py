import requests
from bs4 import BeautifulSoup as bs
import json

response = requests.get("https://docs.python.org/3/contents.html") # Python Complete Page list
html = response.content
contents = bs(html, "html.parser")

links = {}      # Doc -> Number
backlinks = {}  # Number -> Doc
cnt = 0

# Link to Page
for refer in contents.find_all('a', {"class" : "reference internal"}):
    href = refer["href"]
    # Assume Library & Reference have contents
    if (("library" in href) == True or ("reference" in href) == True) and ('#' in href) == False and links.get(href) == None:
        links[href] = cnt
        backlinks[cnt] = href
        cnt += 1

        response = requests.get("https://docs.python.org/3/" + href) # Contents Page
        html = response.content
        doc = bs(html, "html.parser")
        
        # Link to content title
        for header in doc.find_all('a', {"class" : "headerlink"}):
            link = header["href"]
            if ('#' in link) == True and links.get(href + link) == None:
                links[href + link] = cnt
                backlinks[cnt] = href + link
                cnt += 1

with open("./Pymaker/datas/pythonDocToNumber.txt", 'w') as f:
    f.write(str(links))

with open("./Pymaker/datas/numberToPythonDoc.txt", 'w') as f:
    f.write(str(backlinks))