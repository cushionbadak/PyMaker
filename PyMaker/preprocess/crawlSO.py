import urllib.request
import time
import re
from bs4 import BeautifulSoup

# Object1 : scrap python-related urls in stackoverflow
# Object2 : from results of object1, get question and answers which has "*docs.python.org/3/*"

# results of Object1 goes to "Python_QNA_URLs.txt"
# results of Object2 goes to "Python_DOC_referURLs.txt"

SourceRootDirectoryName = "../"
Object1_DirectoryName = SourceRootDirectoryName + "./datas/object1/RawURL/"
Object1_Filename_Prefix = "Python_QNA_URLs_"
Object1_Filename_Postfix = ".txt"
Object2_DirectoryName = SourceRootDirectoryName + "./datas/object2/RawHTML/"
Object2_Filename_Prefix = "Python_DOC_referPages."
Object2_Filename_Postfix = ".txt"
StackOverflow_URL_Prefix = "https://stackoverflow.com"

Object2_LogfileName_Prefix = "datas/object2/run2log/log_"
Object2_LogfileName_Postfix = ".txt"

FirstURLPrefix = "https://stackoverflow.com/questions/tagged/python?sort=newest&page="
FirstUrlPostfix = "&pagesize=50"

PythonDocURL = "docs.python.org/3/"

def Object1_Filename_Gen(prefix, startPageNum, endPageNum):
    return prefix + Object1_Filename_Prefix + str(startPageNum) + '_' + str(endPageNum) + Object1_Filename_Postfix

def Extract_SO_QuestionName_from_URL(url):
    # source: https://stackoverflow.com/a/21360721
    try:
        _, var2 = re.search(r"\/questions\/([0-9]+)\/([a-z0-9\-]+)", url).groups()
    except:
        _, var2 = '00000000', 'na'
    return var2

def Object2_Filename_Gen(prefix, url):
    return prefix + Object2_Filename_Prefix + Extract_SO_QuestionName_from_URL(url) + Object2_Filename_Postfix

def Object2_LogfileName_Gen(prefix, startNum):
    return prefix + Object2_LogfileName_Prefix + str(startNum) + Object2_LogfileName_Postfix

def Run1(startPageNum, endPageNum, isAppend=True):
    if(isAppend):
        fileOpenFlag = "a"
    else:
        fileOpenFlag = "w"

    Object1_Filename = Object1_Filename_Gen(Object1_DirectoryName, startPageNum, endPageNum)
    f1 = open(Object1_Filename, fileOpenFlag)
    for i in range(startPageNum, endPageNum + 1):
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
    # Read URL
    inputFileName = Object1_Filename_Gen(Object1_DirectoryName, startPageNum, endPageNum)
    with open(inputFileName, 'r') as inputFile:
        urls = inputFile.readlines()
    urls = [(StackOverflow_URL_Prefix + x.strip()) for x in urls]
    
    # For each URL, if it is valid URL, scrap its valid 
    # Condition of Valid URL:
    #   - one or more answers
    #   - its body contains a link to 'PythonDocURL'

    # this 'index' variable is used for logging.
    index = 0

    logFileName = Object2_LogfileName_Gen(SourceRootDirectoryName, startPageNum)
    with open(logFileName, 'w') as logFile:
        for url in urls:
            index += 1
            logFile.flush()

            # SLEEP
            time.sleep(1)

            try:
                # if write success, validWrite turns on to True.
                # variable 'validWrite' is for Logging purpose.
                validWrite = False

                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, features='html.parser')

                # NOTE : This classification does not consider scores.
                post_texts = soup.find_all('div', 'post-text')
                comments = soup.find_all('span', 'comment-copy')

                # Check whether the contents is valid.
                if len(post_texts) != 1 and soup.find(PythonDocURL) != -1:
                    # Open File for writing.
                    outputFileName = Object2_Filename_Gen(Object2_DirectoryName, url)
                    with open(outputFileName, 'w') as outputFile:
                        for post in post_texts:
                            outputFile.write(str(post) + '\n')
                        for comment in comments:
                            outputFile.write(str(comment) + '\n')
                        validWrite = True
                        outputFile.flush()

                # Logging
                if validWrite:
                    logFile.write('Complete\t: index = ' + str(index) + '\n')
                else:
                    logFile.write('Removed\t\t: index = ' + str(index) + '\n')
                logFile.write('\t' + url + '\n')

            except:
                # Logging
                logFile.write('Exception\t: index = ' + str(index) + '\n')
                logFile.write('\t' + url + '\n')
