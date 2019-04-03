import urllib.request
import time
from bs4 import BeautifulSoup

# Object1 : scrap python-related urls in stackoverflow
# Object2 : from results of object1, get question and answers which has "*docs.python.org/3/*"

# results of Object1 goes to "Python_QNA_URLs.txt"
# results of Object2 goes to "Python_DOC_referURLs.txt"

Object1_DirectoryName = "./datas/RawUrl/Python_QNAS/"
Object1_Filename_Prefix = "Python_QNA_URLs_"
Object1_Filename_Postfix = ".txt"
Object2_DirectoryName = "./datas/object2/RawHTML/"
Object2_Filename_Prefix = "Python_DOC_referURLs_"
Object2_Filename_Postfix = ".txt"
StackOverflow_URL_Prefix = "https://stackoverflow.com"

FirstURLPrefix = "https://stackoverflow.com/questions/tagged/python?sort=newest&page="
FirstUrlPostfix = "&pagesize=50"

PythonDocURL = "docs.python.org/3"

def Object1_Filename_Gen(prefix, startPageNum, endPageNum):
    return prefix + Object1_Filename_Prefix + str(startPageNum) + '_' + str(endPageNum) + Object1_Filename_Postfix

def Object2_Filename_Gen(prefix, startPageNum, endPageNum):
    return prefix + Object2_Filename_Prefix + str(startPageNum) + '_' + str(endPageNum) + Object2_Filename_Postfix

def Run1(startPageNum, endPageNum, isAppend=True):
    if(isAppend):
        fileOpenFlag = "a"
    else:
        fileOpenFlag = "w"

    Object1_Filename = Object1_Filename_Gen(Object1_DirectoryName, startPageNum, endPageNum)
    f1 = open(Object1_Filename, fileOpenFlag)
    for i in range(startPageNum, endPageNum):
        urlName = FirstURLPrefix + str(i) + FirstUrlPostfix
        page = urllib.request.urlopen(urlName)
        soup = BeautifulSoup(page, features='html.parser')
        question_hyperlinks = soup.find_all('a', 'question-hyperlink')
        
        for k in question_hyperlinks:
            href = k['href']
            if not 'https://' in href:
                f1.write(href + '\n')
    f1.close()

def Run2(startPageNum, endPageNum, isAppend=False):
    inputFileName = Object1_Filename_Gen(Object1_DirectoryName, startPageNum, endPageNum)
    with open(inputFileName, 'r') as inputFile:
        urls = inputFile.readlines()
    urls = [(StackOverflow_URL_Prefix + x.strip()) for x in urls]
    #outputFileName = Object2_Filename_Prefix + outputFileNameMiddleStr + Object1_Filename_Postfix
    outputFileName = Object2_Filename_Gen(Object2_DirectoryName, startPageNum, endPageNum)
    with open(outputFileName, 'w') as outputFile:
        index = 0 
        for url in urls:
            index += 1

            # SLEEP
            time.sleep(0.5)

            try:
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, features='html.parser')

                post_texts = soup.find_all('div', 'post-text')
                comments = soup.find_all('span', 'comment-copy')

                print("Run2 - Info : " + url + "\n" + str(index) + " : post_size = " + str(len(post_texts)) + ", comment_size = " + str(len(comments)))
                if len(post_texts) == 1 and len(comments) == 0:
                    continue

                # Write File
                for post in post_texts:
                    if post.find(PythonDocURL) != -1:
                        outputFile.write(str(post) + '\n')
                for comment in comments:
                    if comment.find(PythonDocURL) != -1:
                        outputFile.write(str(comment) + '\n')
            except:
                print("Run2 - Exception : " + url)
