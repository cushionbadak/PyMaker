import sys

from obj3_datasearch import *
from pymaker_service import *


filestrings = []
allfilelist = obj3_allfilelist()
for i in range(len(allfilelist)):
    questfile = allfilelist[i]
    quest = questfile.split("Python_DOC_referPages.")[1]
    quest = quest[:-4].replace('-', ' ')
    filestrings.append(quest)


def obj3_getanswer_urls(allfilelist_index):
    _, a = obj3_readfile(allfilelist[allfilelist_index])
    return list(set([num2pydoc[k].split('#')[0] for k in a]))

print('obj3_test.py: test start')
correctcount = []
answercount = []
test_iter = 0
for i in range(len(filestrings)):
    test_iter += 1
    fs = filestrings[i]
    answers = obj3_getanswer_urls(i)
    candidates = evaluate_query(fs, n=5, longURL=True, upperdoc=True)
    candidates = ['/'.join(url.split('/')[4:]) for url in candidates]
    co = sum([answers.count(can) for can in candidates])

    correctcount.append(co)
    answercount.append(len(answers))
    
    print('ITEATION ' + str(test_iter) + ' =>\tCORRECT: ' + str(
        co) + ' / ' + str(len(answers)) + '\t\tQUERY: ' + fs)
    print('CANDIDATES:')
    for can in candidates:
        print('\t' + can)
    print('ANSWERS:')
    for a in answers:
        print('\t' + a)
print('TOTAL CORRECT: ' + str(sum(correctcount)) + ' / ' + str(sum(answercount)) + '\n')
print('')
print('obj3_test.py: test finish')
