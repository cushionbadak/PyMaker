import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests
from bs4 import BeautifulSoup as bs

from random import randint
from time import sleep

from lt2.obj3_datasearch import *


googleurl = "https://www.google.com/search?q=site:docs.python.org/3/+"
duckurl = "https://duckduckgo.com/search?q=site:docs.python.org/3/+"
pydocurl = "https://docs.python.org/3/"


def search(engineurl):
    headers = {'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}

    correctcount = []
    answercount = []

    allfilelist = obj3_allfilelist()
    for i in range(len(allfilelist)):
        questfile = allfilelist[i]
        quest = questfile.split("Python_DOC_referPages.")[1][:-4].replace('-', '+')

        response = None
        if engineurl == "google":
            response = requests.get(googleurl + quest, headers=headers)
        elif engineurl == "duckduckgo":
            response = requests.get(duckurl + quest, headers=headers)
        html = response.content
        contents = bs(html, "html.parser")

        results = None
        if engineurl == "google":
            results = contents.find_all("h3", {"class" : 'r'})[:5]
        elif engineurl == "duckduckgo":
            results = contents.find_all('a', {"class" : "result__a"})[:5]
        searchlist = []
        for result in results:
            rawurl = None
            if engineurl == "google":
                rawurl = result.select('a')[0]["href"].split('&')[0][7:].split('%3F')[0]
            elif engineurl == "duckduckgo":
                pass
            url = pydocurl + '/'.join(rawurl.split('/')[4:])
            searchlist.append(url)
        searchlist = list(set(searchlist))

        _, answerurls = obj3_readfile(allfilelist[i])
        answerlist = list(set([pydocurl + num2pydoc[k].split('#')[0] for k in answerurls]))


        co = sum([answerlist.count(can) for can in searchlist])
        correctcount.append(co)
        answercount.append(len(answerlist))

        print('ITEATION ' + str(i + 1) + ' =>', end='\t')
        print('CORRECT: ' + str(co) + ' / ' + str(len(answerlist)), end='\t\t')
        print('QUERY: ' + quest.replace('+', ' '))
        print('CANDIDATES:')
        for can in searchlist:
            print('\t' + can)
        print('ANSWERS:')
        for a in answerlist:
            print('\t' + a)

        rand_value = randint(1, 5)
        sleep(rand_value)

    print('TOTAL CORRECT: ' + str(sum(correctcount)) + ' / ' + str(sum(answercount)) + '\n')
    print()
    print('test finish')