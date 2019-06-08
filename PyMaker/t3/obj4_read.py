
from . import string_util
from . import t3_global


def obj4_filename(n, includepath=True):
    # n : int. (0 <= n < 10655)
    # output : string
    # example (depends on t3_global.OBJ4_DATAPATH) : obj4_filename(3, True) => 'PyMakers/datas/object4/1st/3.txt'
    return (t3_global.OBJ4_DATAPATH if includepath else '') + str(n) + '.txt'


def obj4_allfilelist(includepath=True):
    # output : string list.
    # obj4_allfilename(True)'s result can be used for obj4_str's argument.
    return [obj4_filename(n, includepath) for n in range(t3_global.OBJ4_SIZE)]


def obj4_str(filename):
    # filename : string (it should include path information.)
    # output : (string, string list) : url, content(string_util.formatsplit filtered word-sequence)
    # input example : 'PyMakers/datas/object4/1st/3.txt'
    # output example : ('reference/introduction.html#introduction', ['This', 'reference', 'manual', ...])

    link = ''
    content = ''

    with open(filename, 'r', encoding='utf-8') as fp:
        i = 0
        for line in fp:
            if i == 1:
                link = str.rstrip(line)
            elif i > 3:
                content += ' ' + line
            i += 1

    return link, string_util.formatsplit(content)


def obj4_linklist():
    # output : string list. its' index is equal to object4's filename.
    linklist = []
    for i in range(t3_global.OBJ4_SIZE):
        with open(obj4_filename(i), 'r', encoding='utf-8') as fp:
            i = 0
            for line in fp:
                if i == 1:
                    linklist.append(str.rstrip(line))
                    break
                i += 1
    return linklist


def obj4_vecrep_filename(n, includepath=True):
    # output : string. (pathname depends on t3_global.OBJ4_VECREP_PATH)
    # example : obj4_vecrep_filename(3, True) => 'PyMaker/datas/object4_subword_vecrep/3'
    # when you save numpy array to file, numpy automatically appends '.npy' at the end of the filename.
    # when you load file to numpy array, you need to append '.npy' to the filename manually.
    return (t3_global.OBJ4_VECREP_PATH if includepath else '') + str(n)



