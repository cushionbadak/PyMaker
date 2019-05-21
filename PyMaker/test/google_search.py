import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests
from bs4 import BeautifulSoup as bs

from time import sleep

from lt2.obj3_datasearch import *


f = open("PyMaker/test/accuracy.txt", 'w')

googleurl = "https://www.google.com/search?q=site:docs.python.org/3/+"
pydocurl = "https://docs.python.org/3/"

correctcount = []
answercount = []

allfilelist = obj3_allfilelist()
for i in range(len(allfilelist)):
    questfile = allfilelist[i]
    quest = questfile.split("Python_DOC_referPages.")[1][:-4].replace('-', '+')

    response = requests.get(googleurl + quest)
    print(response)
    html = response.content
    contents = bs(html, "html.parser")

    results = contents.find_all("h3", {"class" : 'r'})[:5]
    googlelist = []
    for result in results:
        rawurl = result.select('a')[0]["href"].split('&')[0][7:]
        url = pydocurl + '/'.join(rawurl.split('/')[4:])
        googlelist.append(url)
    googlelist = list(set(googlelist))

    _, answerurls = obj3_readfile(allfilelist[i])
    answerlist = list(set([pydocurl + num2pydoc[k].split('#')[0] for k in answerurls]))


    co = sum([answerlist.count(can) for can in googlelist])
    correctcount.append(co)
    answercount.append(len(answerlist))

    print('ITEATION ' + str(i + 1) + ' =>', end='\t')
    print('CORRECT: ' + str(co) + ' / ' + str(len(answerlist)), end='\t\t')
    print('QUERY: ' + str(len(questfile)))
    print('CANDIDATES:')
    for can in googlelist:
        print('\t' + can)
    print('ANSWERS:')
    for a in answerlist:
        print('\t' + a)
    sleep(0.05)

print('TOTAL CORRECT: ' + str(sum(correctcount)) + ' / ' + str(sum(answercount)) + '\n')
print()
print('obj3_test.py: test finish')

f.close()