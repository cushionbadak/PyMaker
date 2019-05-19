import sys
import string

from lt2_global import *
sys.path.append('../learning')
from datasearch import *

_ALPHA_NUM_WS = string.ascii_letters + string.digits + string.whitespace

def alphanumws_converter(c, replace=' '):
    # c : character (length-1 string)

    # Examples :
    #   alphanumws_converter('a') => 'a'
    #   alphanumws_converter('\n') => '\n'
    #   alphanumws_converter('2') => '2'
    #   alphanumws_converter(' ') => ' '
    #   alphanumws_converter('_') => ' '
    return c if c in _ALPHA_NUM_WS else replace


def formatsplit(s):
    # s : string (whole bunch of contents)
    # output : string list

    # Example using alphanumws_converter :
    #   formatsplit('as3 ][3i] z-12 p.pow')
    #   => ['as3', '3i', 'z', '12', 'p', 'pow']

    # To change its' behavior, you should change alphanumws_converter to other function.
    return ''.join(list(map(alphanumws_converter, s))).split()


def obj4_filename(n, includepath=True):
    # n : int. (0 <= n < 10655)
    return (OBJ4_PATH if includepath else '') + str(n) + '.txt'


def obj4_allfilename():
    return [obj4_filename(n) for n in range(0, 10655)]


def obj4_str(filename):
    # filename : string (it should include path information.)
    # output : (string, string list) : link, content(filtered word-sequence).

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

    return link, formatsplit(content)


def obj4_vecrep_filename(n, includepath=True):
    return (OBJ4_VECREP_PATH if includepath else '') + str(n)
