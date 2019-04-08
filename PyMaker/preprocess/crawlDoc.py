import requests
from bs4 import BeautifulSoup as bs

response = requests.get("https://docs.python.org/3/contents.html")
html = response.content
contents = bs(html, "html.parser")

links = []

for refer in contents.find_all('a', {"class" : "reference internal"}):
    href = refer["href"]
    if ('#' in href) == False and links.count(href) == 0:
        links.append(href)

        response = requests.get("https://docs.python.org/3/" + href)
        html = response.content
        doc = bs(html, "html.parser")
        
        print(doc.title)

        