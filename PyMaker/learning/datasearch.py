import os
import re

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


def read_obj3file(filename):
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
    with open(filepath, 'r') as f:
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
