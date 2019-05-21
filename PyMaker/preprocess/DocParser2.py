from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
import sys

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
    formatStr = "{0:." + str(decimals) + "f}" 
    percent = formatStr.format(100 * (iteration / float(total))) 
    filledLength = int(round(barLength * iteration / float(total))) 
    bar = '#' * filledLength + '-' * (barLength - filledLength) 
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)), 
    if iteration == total: 
        sys.stdout.write('\n') 
    sys.stdout.flush()

docsList =[]
dataPath = "../datas/object4/2nd/"
with open("../datas/numberToPythonDoc.txt", 'r') as f:
    data = f.read()
    docsList = eval(data)
cnt = 0
for idx, docslink in docsList.items():
    s_idx = 0       # there is no 0 value in docsList. 0 is initial value
    if '#' in docslink:
        s_idx = docslink.index('#')
    bs = BeautifulSoup(urlopen('https://docs.python.org/3/' + docslink), 'html.parser')
    for pre in bs("pre"):
        pre.decompose()
    for code in bs("code"):
        code.decompose()
    if s_idx == 0:
        f = open(dataPath + str(idx) + '.txt', mode = 'w', encoding = 'utf-8')
        f.write('link:\n' + docslink + '\n\n' + 'docs:' + '\n')
        target_bs = bs.find('div', attrs = {'class' : "body", 'role' : "main"})
        f.write(target_bs.get_text())
        f.close()
        cnt += 1
    else:
        idName = docslink[s_idx+1:]        #tag's name
        target_bs = bs.find(attrs= {'id' : idName})
        f = open(dataPath + str(idx) + '.txt', mode = 'w', encoding = 'utf-8')
        if target_bs.name == 'div':
            f.write('link:\n' + docslink + '\n\n' + 'docs:' + '\n')
            f.write(target_bs.get_text())
            f.close()
            cnt += 1
        elif target_bs.name == 'dt':
            f.write('link:\n' + docslink + '\n\n' + 'docs:' + '\n')
            f.write(target_bs.find_parent().get_text())
            f.close()
            cnt += 1
    printProgress(cnt, len(docsList), 'Progress:', 'Complete', 1, 50)

    

''' ↓test
url = "https://docs.python.org/3/library/stdtypes.html#memory-views"
bs = BeautifulSoup(urlopen(url), 'html.parser')

###in case of long paragraph
s_idx = url.index('#')
sub_url = url[s_idx+1:]   #tag's name
target_bs = bs.find("div", id = sub_url)
# every text(comprise code): target_bs.get_text()
# code-extracted-version: add [for pre in target_bs("pre"):  pre.decompose()]
# bs.find에 .name 하면 맨 앞 태그 나옴. 지금 큰거면 div고 작은거면(큰거 안에) dt니까 이걸로 검사하면 됨
test = bs.find(id = "memoryview")
print(test.name)
#print(test)
f = open('test.txt', 'w')
for item in test.find_parent():
    f.write(str(item))
f.close()'''
