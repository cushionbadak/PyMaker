import numpy as np
from scipy import linalg, dot

from . import t3_global
from . import string_util
from . import obj3_read
from . import obj4_read


def save_all_obj4_docvec(docvec_func, allowpickle_val=False):
    # docvec_func : string list -> numpy array. the way to make a vector
    # allowpickle_val : bool.
    # No output value.
    # Side effect: create over 10000 numpy vector files at t3_global.OBJ4_VECREP_PATH
    _printlog = t3_global.OBJ4_VECREP_CALC_SAVE_DOCVEC_PRINT_LOG
    if _printlog:
        print('obj4_vecrep_calc.py: start save_all_obj4_docvec at ' + t3_global.OBJ4_VECREP_PATH)
    for i in range(t3_global.OBJ4_SIZE):
        _, content = obj4_read.obj4_str(obj4_read.obj4_filename(i, includepath=True))
        ofilename = obj4_read.obj4_vecrep_filename(i)

        # If you want to change the way to make a vector representation, modify below line.
        # ex) np.save(ofilename, google_w2v.unigram_sentence_wordvecsum())
        np.save(ofilename, docvec_func(content), allow_pickle=allowpickle_val)
    if _printlog:
        print('obj4_vecrep_calc.py: end save_all_obj4_docvec')


def load_all_obj4_docvec(allowpickle_val=False):
    # preprocessing
    # allowpicle_val : bool.
    # output d : dict(int, (numpy.ndarray, float))
    # dict (obj4-index, (vector-rep, vector-size))
    d = dict()
    for i in range(t3_global.OBJ4_SIZE):
        na = np.load(obj4_read.obj4_vecrep_filename(i, includepath=True) + '.npy', allow_pickle=allowpickle_val)
        d[i] = (na, linalg.norm(na))
    return d


# initialize
# obj4_docvec : dict(int, (numpy.ndarray, float))
#   dict(obj4-index, (vector-rep, vector-size))
# obj4_urllist : string list (index: obj4-index, element: url)
# obj4_url2num : dict(string, int) (reverse of obj4_urllist)
obj4_docvec = {}
obj4_urllist = []
obj4_url2num = {}


if t3_global.OBJ4_VECREP_CALC_SET_GLOBAL_VARIABLES:
    _printlog = t3_global.OBJ4_VECREP_CALC_SET_GLOBAL_VARIABLES_PRINT_LOG
    if _printlog:
        print('obj4_vecrep_calc.py: set obj4_docvec and obj4_urllist')
    obj4_urllist = obj4_read.obj4_linklist()
    obj4_url2num = dict(zip(obj4_urllist, range(len(obj4_urllist))))
    obj4_docvec = load_all_obj4_docvec(t3_global.OBJ4_VECREP_CALC_ALLOW_PICKLE)
    if _printlog:
        print('obj4_vecrep_calc.py: finish set obj4_docvec and obj4_urllist')


def get_cosine(av, bv, avs, bvs):
    # av : numpy array
    # bv : numpy array
    # avs : float. length of av
    # bvs : float. length of bv
    # output : float.
    return (dot(av, bv)/avs/bvs).item()

def get_cosine_values_alldoc(ws, docvec_func):
    # ws : string list (well-preprocessed, like output of obj4_read.formatsplit())
    # docvec_func : string list -> numpy array. the way to make a vector
    # output : dict(int, float). dict(obj4-index, cosinevalue). dict of all cosine values of python documents.
    vr = docvec_func(ws)
    vrs = linalg.norm(vr)

    l = {}
    for i in range(len(obj4_urllist)):
        pydocvr, pydocvrs = obj4_docvec[i]
        l[i] = get_cosine(vr, pydocvr, vrs, pydocvrs)
    return l


def get_cosine_values_upperdoc(ws, docvec_func):
    # ws, docvec_func : refer get_cosine_values_alldoc's ws, docvec_func, repectively.
    # output : dict(int, float). dict(obj4-index, cosinevalue). dict of all cosine values of python upper-documents.
    vr = docvec_func(ws)
    vrs = linalg.norm(vr)

    l = {}
    for url in obj3_read.upperpydocset:
        obj4index = obj4_url2num[url]
        pydocvr, pydocvrs = obj4_docvec[obj4index]
        l[obj4index] = get_cosine(vr, pydocvr, vrs, pydocvrs)
    return l


#def cosine_filter(d, cos_lowlimit):
#    # d : dict(int, float). dict(obj4-index, cosinevalue)
#    # cos_lowlimit : float.
#    # output : dict(int, float). dict(obj4-index, cosinevalue).
#    return dict((k, v) for k, v in d.items() if v > cos_lowlimit)


def cosine_filter(d, cos_width):
    # d : dict(int, float). dict(obj4-index, cosinevalue)
    # cos_width : float.
    # output : dict(int, float). dict(obj4_index, cosinevalue).
    cos_maxvalue = max(d.values())
    cos_lowlimit = cos_maxvalue - cos_width
    return dict((k, v) for k, v in d.items() if v > cos_lowlimit)

def binary_classification_alldoc(answers, candidates):
    # answers : string set (pydoc urls)
    # candidates : string set (pydoc urls)
    # answers are (false negative or true positive)
    # candidates are Positive. (len(obj3_read.pydoc2num) - len(candidates)) are the # of Negative.
    # OUTPUT
    # all output values are integer.
    # tp : # of True Positive
    # fp : # of False Positive
    # fn : # of False Negative
    # tn : # of True Negative
    tp = sum(1 for url in candidates if url in answers)
    fp = len(candidates) - tp
    fn = len(answers) - tp
    tn = len(obj3_read.pydoc2num) - tp - fp - fn
    return tp, fp, fn, tn



def binary_classification_upperdoc(answers, candidates):
    # answers : string set (upperdoc urls)
    # candidates : string set (upperdoc urls)
    # answers are (false negative or true positive)
    # candidates are Positive. (len(obj3_read.upperpydocset) - len(candidates)) are the # of Negative.
    # OUTPUT
    # all output values are integer.
    # tp : # of True Positive
    # fp : # of False Positive
    # fn : # of False Negative
    # tn : # of True Negative
    tp = sum(1 for url in candidates if url in answers)
    fp = len(candidates) - tp
    fn = len(answers) - tp
    tn = len(obj3_read.upperpydocset) - tp - fp - fn
    return tp, fp, fn, tn
