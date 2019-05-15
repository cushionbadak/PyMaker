from os import listdir
from os.path import isfile, join, split

# datas/object3/ folder should be unzipped like this.
# [project_root]/PyMaker/datas/object3/1st/i501/Python_DOC_referPages.accept-file-and-pass-arguments-to-function-from-command-line-gives-no-output.txt

_DATAPATH = '../datas/'
_OBJ3_DATAPATH = _DATAPATH + 'object3/'

pydoc2num = {}
num2pydoc = {}

with open(_DATAPATH + 'pythonDocToNumber.txt', 'r') as f:
    _temp_data = f.read()
    pydoc2num = eval(_temp_data)


with open(_DATAPATH + 'numberToPythonDoc.txt', 'r') as f:
    _temp_data = f.read()
    num2pydoc = eval(_temp_data)


def obj3_readfile(filename):
    # filename : filename its' path under 'object3'.
    # for exmample, argument 'sample_i1/hello.txt' for '[project_root]/PyMaker/datas/object3/sample_i1/hello.txt'

    # OUTPUT
    # contentstr : string
    # answerurls : int list

    # status (simple-DFA)
    # 0 : before reading
    # 1 : reading 'Natural Text' part
    # 2 : reading 'Answer URL' part
    filepath = _DATAPATH + 'object3/' + filename
    urlheadlen = len('https://docs.python.org/3/')
    contentstr = ''
    answerurls = []
    status = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if status == 1:
                if 'Answer URL' in line:
                    status = 2
                else:
                    contentstr += line
            elif status == 0:
                if 'Natural Text' in line:
                    status = 1
            elif status == 2:
                try:
                    answerurls.append(pydoc2num[str.rstrip(line[urlheadlen:])])
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
    pathname = _OBJ3_DATAPATH + foldernametail
    return [(foldernametail + f) for f in listdir(pathname) if isfile(join(pathname, f))]


def obj3_allfilelist():
    # output : string list.
    #  specific output list element string format is written at obj3_getfilelist function's comment.
    r = []
    for i in range(0, 226):
        r.extend(obj3_getfilelist(i))
    return r


def obj3_getdistinctfilename(filename):
    # every obj3's filename contains 'Python_DOC_referPages.' and '.txt'
    # this function removes it.
    _, tailfilename = split(filename)
    return tailfilename[22:-4]