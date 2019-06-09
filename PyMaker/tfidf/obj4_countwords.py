import pickle
from math import log

# import modules from sibling directory.
# https://stackoverflow.com/a/9806045
# https://stackoverflow.com/a/27876800
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from t3.obj4_read import *
import tfidf_g


if tfidf_g.OBJ4_WC_RUN:
    # Count every words in python official documents and pickle it.
    # pickle dump and load: https://stackoverflow.com/a/11218504
    o4_afl = obj4_allfilelist(includepath=True)
    dfc = dict()

    for i in range(tfidf_g.OBJ4_SIZE):
        tfc = dict()
        _, s = obj4_str(o4_afl[i])
        for w in s:
            if w in tfc:
                tfc[w] += 1
            else:   
                if w in dfc:
                    dfc[w] += 1
                else:
                    dfc[w] = 1
                tfc[w] = 1
        with open(tfidf_g.obj4_wc_doccount_dict_filename(i), 'wb') as countfile:
            pickle.dump(tfc, countfile)

    with open(tfidf_g.OBJ4_WC_TOTALCOUNT_DICT_FILENAME, 'wb') as totalcountfile:
        pickle.dump(dfc, totalcountfile)

obj4_dfc = dict()
dfcsum = 0
if tfidf_g.OBJ4_WC_TOTAL_LOAD:
    with open(tfidf_g.OBJ4_WC_TOTALCOUNT_DICT_FILENAME, 'rb') as totalcountfile:
        obj4_dfc = pickle.load(totalcountfile)
dfcsum = sum(obj4_dfc.values())



def load_obj4_tfc(n):
    # n : int (obj4 filenumber)
    # output : int, dict {string : int}
    tfc = dict()
    filename = tfidf_g.obj4_wc_doccount_dict_filename(n)
    with open(filename, 'rb') as countfile:
        tfc = pickle.load(countfile)
    return sum(tfc.values()), tfc


def tfidf (tf, df, base=2.0):
    # tf : float. term freq
    # df : float. document freq
    # base : float. log base.
    # output : float. tf * idf
    
    # return log(tf/ (df + 1))
    return log(tf / df, base)