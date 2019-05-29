import re
from os import listdir
from os.path import isfile, join, split

from . import t3_global


# initialize
pydoc2num = {}
num2pydoc = {}
upperpydocset = set()
upperpydoc2num = {}
num2upperpydoc = {}
pydoc2upperpydocnum = {}


def getupperpydoc(s):
    # s : string. string in pydoc2num's key.
    # output : string. input url's postfix deleted.
    # example : 'reference/introduction.html#introduction' => 'reference/introduction.html'
    return re.sub('#.*', '', s)


if t3_global.OBJ3_READ_SET_GLOBAL_VARIABLES:
    _printlog = t3_global.OBJ3_READ_SET_GLOBAL_VARIABLES_PRINT_LOG
    if _printlog:
        print('obj3_read.py: start writing dictionaries')
    with open(t3_global.PYTHONDOCTONUM, 'r') as f:
        _temp_data = f.read()
        pydoc2num = eval(_temp_data)

    with open(t3_global.NUMTOPYTHONDOC, 'r') as f:
        _temp_data = f.read()
        num2pydoc = eval(_temp_data)

    upperpydocset = set([getupperpydoc(p) for p in pydoc2num])
    upperpydoc2num = dict(zip(upperpydocset, range(len(upperpydocset))))
    num2upperpydoc = dict((v, k) for k, v in upperpydoc2num.items())
    pydoc2upperpydocnum = dict((k, upperpydoc2num[getupperpydoc(k)]) for k, v in pydoc2num.items())
    if _printlog:
        print('obj3_read.py: end writing dictionaries')


def obj3_readfile(filename, return_upperpydocnum=False):
    # filename : filename its' path under 'object3'.
    #   for exmample, argument filename='sample_i1/hello.txt' to read '[project_root]/PyMaker/datas/object3/sample_i1/hello.txt'
    # return_upperpydocnum : it determines 'answerurls' 's meaning.
    #   if True, it returns integer list filled with index in num2upperpydoc.
    #   if False, it returns integer list filled with index in num2pydoc.
    
    # OUTPUT
    # contentstr : string
    # answerurls : int list
    
    # variable 'status' (sipmle-DFA)
    # 0 : before reading
    # 1 : reading 'Natural Text' part
    # 2 : reading 'Answer URL' part
    filepath = t3_global.OBJ3_DATAPATH + filename
    urlheadlen = len(t3_global.PYDOCURL)
    contentstr = ''
    answerurls = []
    status = 0
    ansurlclass = pydoc2upperpydocnum if return_upperpydocnum else pydoc2num

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if status == 1:
                if t3_global.OBJ3_READ_ANSWERURL_DELIM in line:
                    status = 2
                else:
                    contentstr += line
            elif status == 0:
                if t3_global.OBJ3_READ_ANSWERURL_DELIM in line:
                    status = 1
            elif status == 2:
                try:
                    answerurls.append(ansurlclass[str.rstrip(line[urlheadlen:])])
                except:
                    pass
            else:
                pass
    return contentstr, answerurls


def obj3_getfilelist(foldernumber):
    # foldernumber : int (range: [0, 225])
    # output : string list.
    #   (string: includes path from object3.)
    #   e.g. 'datas/object3/1st/i501/hello.txt' => OUTPUT : ['1st/i501/hello.txt', ...]

    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    foldernametail = '1st/i' + str(foldernumber * 100 + 1) + '/'
    pathname = t3_global.OBJ3_DATAPATH + foldernametail
    return [(foldernametail + f) for f in listdir(pathname) if isfile(join(pathname, f))]


def obj3_allfilelist():
    # output : string list. e.g. 'PyMaker/datas/object3/1st/i501/hello.txt'
    #   specific output list element string format is written at obj3_getfilelist function's comment.
    r = []
    for i in range(t3_global.OBJ3_FOLDER_COUNT):
        r.extend(obj3_getfilelist(i))
    return r


def obj3_getdistinctfilename(filename):
    # every obj3's filename contains 'Python_DOC_referPages.' and '.txt'
    # this function removes that prefix and postfix.
    _, tailfilename = split(filename)
    return tailfilename[22:-4]




