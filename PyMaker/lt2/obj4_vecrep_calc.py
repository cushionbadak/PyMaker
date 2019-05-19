from numpy import save
from numpy import load
from scipy import dot, linalg

from lt2_global import *
from obj4_read import *
from google_w2v import *
from obj3_datasearch import *

obj4_link_list = obj4_linklist()
uli = obj4_upperlink_list()


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
    for i in range(0, len(uli)):
        pydocvr, pydocvrs = d[obj4_link_list.index(uli[i])]
        l.append((dot(vr, pydocvr.T)/vrs/pydocvrs).item())
    
    # https://stackoverflow.com/a/7851166
    return [k for k in sorted(range(len(l)), reverse=True, key=lambda k: l[k])[:n]]


def get_top_n_similar_pydoc_from_str(s, d, n=N_FOR_TOP_N_VALUES):
    return get_top_n_similar_pydoc(formatsplit(s), d, n)


def correct_answers_count(candidate, answer):
    answers = [obj4_link_list[a] for a in answer]
    return sum([answers.count(uli[i]) for i in candidate])


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
        
        c, a = obj3_readfile(fn, isupperpydocused=True)
        a = [obj4_link_list.index(num2upperpydoc[aa]) for aa in a]
        gtnsp = get_top_n_similar_pydoc_from_str(c, d, n)
        co = correct_answers_count(gtnsp, a)
        corrects.append(co)
        answercount.append(len(a))

        fntail = obj3_getdistinctfilename(fn)
        print('ITEATION ' + str(test_iter) + ' =>\tCORRECT: ' + str(
            co) + ' / ' + str(len(a)) + '\t\tFILE: ' + fntail)
        
        print('CANDIDATES:')
        for can in gtnsp:
            print('\t' + uli[can])
        print('ANSWERS:')
        for a in a:
            print('\t' + obj4_link_list[a])
    print('TOTAL CORRECT: ' + str(sum(corrects)) + ' / ' + str(sum(answercount)) + '\n')
    print('')

    return
        

d = get_all_obj4_docvec()
test_obj3(d)
