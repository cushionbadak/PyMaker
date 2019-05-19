from numpy import save
from numpy import load
from scipy import dot, linalg

from lt2_global import *
from obj4_read import *
from google_w2v import *
from obj3_datasearch import *


def save_all_obj4_docvec():
    fns = obj4_allfilename()
    for i in range(0, 10655):
        _, c = obj4_str(obj4_filename(i, includepath=True))
        ofilename = obj4_vecrep_filename(i)
        save(ofilename, unigram_sentence_wordvecsum(c))


def get_all_obj4_docvec():
    # preprocessing
    # output : dict(int, (numpy.ndarray, float))
    # dict (index, (vector-rep, vector-size))
    d = dict()
    for i in range(0, 10655):
        na = load(obj4_vecrep_filename(i, includepath=True) + '.npy')
        d[i] = (na, linalg.norm(na))
    return d


def get_top_n_similar_pydoc(ws, d, n=N_FOR_TOP_N_VALUES):
    # ws : string list (well-preprocessed, like output of obj4_read.formatsplit())
    # n : int (top-n)
    # d : return value of get_all_obj4_docvec()
    # output : int list (length-n)

    vr = unigram_sentence_wordvecsum(ws)
    vrs = linalg.norm(vr)

    l = []
    for i in range(0, 10655):
        pydocvr, pydocvrs = d[i]
        l.append((dot(vr, pydocvr.T)/vrs/pydocvrs).item())
    
    # https://stackoverflow.com/a/7851166
    return [l.index(k) for k in sorted(range(len(l)), reverse=True, key=lambda k: l[k])[:n]]


def get_top_n_similar_pydoc_from_str(s, d, n=N_FOR_TOP_N_VALUES):
    return get_top_n_similar_pydoc(formatsplit(s), d, n)


def correct_answers_count(candidate, answer):
    return sum(1 for i in candidate if i in answer)


def test_obj3(d, n=N_FOR_TOP_N_VALUES, testnum=N_FOR_TESTCASE_NUM):
    # d : return value of get_all_obj4_docvec()
    # output : No return value. test log will go to stdout.

    fnl = obj3_allfilelist()
    test_iter = 0
    corrects = []
    answercount = []
    for fn in fnl:
        test_iter += 1
        if testnum > 0 and test_iter > testnum:
            break
        
        c, a = obj3_readfile(fn, isupperpydocused=False)
        gtnsp = get_top_n_similar_pydoc_from_str(c, d, n)
        co = correct_answers_count(gtnsp, a)
        corrects.append(co)
        answercount.append(a)

        fntail = obj3_getdistinctfilename(fn)
        print('ITEATION ' + str(test_iter) + ' =>\tCORRECT: ' + str(
            co) + ' / ' + str(len(a)) + '\t\tFILE: ' + fntail)
        
        print('CANDIDATES:')
        for c in gtnsp:
            print('\t' + num2pydoc[c])
        print('ANSWERS:')
        for a in a:
            print('\t' + num2pydoc[a])
    print('TOTAL CORRECT: ' + str(sum(corrects)) + ' / ' + str(answercount) + '\n')

    return
        

d = get_all_obj4_docvec()
test_obj3(d)
