import requests
from bs4 import BeautifulSoup as bs

response = requests.get("https://docs.python.org/3/contents.html")
html = response.content
contents = bs(html, "html.parser")

links = {}
cnt = 0

for refer in contents.find_all('a', {"class" : "reference internal"}):
    href = refer["href"]
    if ('#' in href) == False and links.get(href) == None:
        links[href] = cnt
        cnt += 1
        print(href, links[href])

        response = requests.get("https://docs.python.org/3/" + href)
        html = response.content
        doc = bs(html, "html.parser")
        
        for header in doc.find_all('a', {"class" : "headerlink"}):
            link = header["href"]
            if ('#' in link) == True and links.get(href + link) == None:
                links[href + link] = cnt
                cnt += 1
                print(href, link, links[href + link])

with open("./Pymaker/datas/pythonDocList.txt", 'w') as f:
    f.write(str(links))
