import sys

from . import t3_global
# Verify whether the evaluation is possible.
if not t3_global.PYMAKER_SERVICE_AVAILABLE:
    print('pymaker_service: t3_global.PYMAKER_SERVICE_AVAILABLE is False value')
    print('pymaker_service: process exit')
    sys.exit()

from . import string_util
from . import obj3_read
from . import obj4_read
from . import obj4_vecrep_calc
from . import google_w2v

# vector representation method.
_docvec_func = google_w2v.subword_sentence_wordvecsum


def classify_query_alldoc(query):
    # query : string (non-preprocessed, just a query string)
    # output : string list. (urls)

    cosine_similarities = obj4_vecrep_calc.get_cosine_values_alldoc(string_util.formatsplit(query), _docvec_func)
    candidates = obj4_vecrep_calc.cosine_filter(cosine_similarities, t3_global.PYMAKER_SERVICE_COS_LOWLIMIT)
    candidates = set([obj4_vecrep_calc.obj4_urllist[k] for k, v in candidates])

    return list(candidates)


def classify_query_upperdoc(query):
    # query : string (non-preprocessed, just a query string)
    # output : string list. (upperdoc urls)

    cosine_similarities = obj4_vecrep_calc.get_cosine_values_upperdoc(string_util.formatsplit(query), _docvec_func)
    candidates = obj4_vecrep_calc.cosine_filter(cosine_similarities, t3_global.PYMAKER_SERVICE_COS_LOWLIMIT)
    candidates = set([obj4_vecrep_calc.obj4_urllist[k] for k, v in candidates])

    return list(candidates)


def evaluate_query(query, longURL=t3_global.PYMAKER_SERVICE_LONGURL, upperdoc=t3_global.PYMAKER_SERVICE_UPPERDOC):
    # query : string
    # longURL : bool
    # upperdoc : bool
    # output : string list
    try:
        if(upperdoc):
            candidates = classify_query_upperdoc(query)
        else:
            candidates = classify_query_alldoc(query)
            return [t3_global.PYDOCURL + c for c in candidates]
    except:
        return []
    