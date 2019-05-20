from numpy import save
from numpy import load
from scipy import dot, linalg

from lt2_global import *
from obj4_read import *
from google_w2v import *
from obj3_datasearch import *
from obj4_vecrep_calc import *


################## HOW TO USE ##########################
# -1. Make sure that PyMaker/lt2, PyMaker/datas/object4_wv_rep/,
#      PyMaker/datas/GoogleNews/ contains appropriate files to run code.
# 0. Check lt2_global.py if you want to configure service easily.
#      They can be manipulated as function arguments too.
# 1. from pymaker_service import evaluate_query
# 2. (It will take about 2-min and consumes over 2GB memory.)
# 3. answers = evaluate_query('How to print hello world in python?')
# 4. ...
# 5. PROFIT!!!
########################################################



# 'model' from google_w2v is the pre-trained word vector representation.
docvec_dict = get_all_obj4_docvec()

def classify_query(query, n=SERVICE_TOP_N, upperdocsearch=SERVICE_UPPERDOC):
    # query : string (non-preprocessed, just a query string)
    # n : int (# of top-n-candidates)
    # upperdocsearch : whether to find candidates at upper-class documents, or lower-class documents.
    # output : int list (length-n). It represents the index at upperdoclist or lowerdoclist according to 'upperdocsearch' argument.

    query_vec_rep = unigram_sentence_wordvecsum(formatsplit(query))
    query_vec_rep_size = linalg.norm(query_vec_rep)

    similarities = []

    if upperdocsearch:
        for i in range(0, len(uli)):
            pydocvr, pydocvrs = docvec_dict[obj4_link_list.index(uli[i])]
            similarities.append((dot(query_vec_rep, pydocvr.T)/query_vec_rep_size/pydocvrs).item())
    else:
        for i in range(0, OBJ4_SIZE):
            pydocvr, pydocvrs = docvec_dict[i]
            similarities.append((dot(query_vec_rep, pydocvr.T)/query_vec_rep_size/pydocvrs).item())

    # https://stackoverflow.com/a/7851166
    return [k for k in sorted(range(len(similarities)), reverse=True, key=lambda k: similarities[k])[:n]]


def num2url(num, longURL=False, upperdoc=SERVICE_UPPERDOC):
    s = ''
    if upperdoc:
        s = uli[num]
    else:
        s = obj4_link_list[num]
    s = ('https://docs.python.org/3/' if longURL else '') + s
    return s


def evaluate_query(query, n=SERVICE_TOP_N, longURL=True, upperdoc=SERVICE_UPPERDOC):
    try:
        candidates = classify_query(query, n, upperdoc)
        return [num2url(c, longURL, upperdoc) for c in candidates]
    except:
        return []
