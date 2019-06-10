import numpy as np
from scipy import linalg, dot

# import modules from sibling directory.
# https://stackoverflow.com/a/9806045
# https://stackoverflow.com/a/27876800
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import t3.obj4_read
import t3.google_w2v
import t3.string_util

import tfidf_g
import obj4_countwords


# tf, df setup
def get_tf(n):
    # n : int. obj4 document number
    # output : dict { string : float }. term freq
    tfcsum, tfc = obj4_countwords.load_obj4_tfc(n)
    return {k: (v/tfcsum) for k, v in tfc.items()}

dfc = obj4_countwords.obj4_dfc
dfcsum = obj4_countwords.dfcsum
df = {k: (v/dfcsum) for k, v in dfc.items()}


# w2v model
model = t3.google_w2v.model


def word_rep(w):
    # w : string. a word.
    # output : np array.
    if w in model:
        return model[w]
    else:
        initv = t3.google_w2v.zerovector()
        t3.google_w2v.make_nzv(initv)
        return initv


def subword_rep(w):
    # w : string. a word.
    # output : np array
    initv = t3.google_w2v.zerovector()
    lowlimit = tfidf_g.SUBWORD_LENGTH_LOW
    highlimit = tfidf_g.SUBWORD_LENGTH_HIGH
    swlist = t3.string_util.make_subword(w, lowlimit, highlimit)
    if (w in model) and (len(w) < lowlimit or len(w) > highlimit):
        swlist.append(w)
    for sw in swlist:
        if sw in model:
            initv += model[sw]
    
    if not np.any(initv):
        t3.google_w2v.make_nzv(initv)

    return initv


def document_rep(n):
    # n : integerobj4 document number
    # output : np array
    tf = get_tf(n)
    initv = t3.google_w2v.zerovector()
    for w, tfidf_v in tf.items():
        # 1st
        #initv += word_rep(w)
        
        # 2nd
        #if tfidf_v < 0:
        #    continue
        #initv += word_rep(w) * tfidf_v
        
        # 3rd
        if tfidf_v < 0:
            continue
        initv += word_rep(w) * tfidf_v / df[w]

    if not np.any(initv):
        t3.google_w2v.make_nzv(initv)

    return initv




for i in range(tfidf_g.OBJ4_SIZE):
    _, content = t3.obj4_read.obj4_str(t3.obj4_read.obj4_filename(i, includepath=True))
    ofilename = tfidf_g.tfidf_obj4_vecrep_filename(i, includepath=True)
    np.save(ofilename, document_rep(i), allow_pickle=tfidf_g.OBJ4_VECREP_CALC_ALLOW_PICKLE)
