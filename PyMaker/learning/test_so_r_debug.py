import torch
from torch.serialization import load
import os
import sys

from stringhash import str2bigramhashlist
from stringhash import str2unigramhashlist
from datasearch import *

_W_IN_FILENAME = 'result_r/zerobase_learned_full_r_2_w_in.pt'
_W_OUT_FILENAME = 'result_r/zerobase_learned_full_r_2_w_out.pt'
_RESULT_LOG_FILENAME = 'result_r/result_so_zerobase_learned_full_r_3.log'
# THIS MUST BE THE SAME VALUE WITH train_zerobase.py's _C['HASH_BIT_SIZE']
_HASH_BIT_SIZE = 18

_DEBUG_MODE = True
_LAB_SERVER_USE = True
_LAB_SERVER_USE_GPU_NUM = "03"

_N_FOR_TESTCASE_NUM = 10
_N_FOR_TOP_N_VALUES = 5


# GPU setting
if _LAB_SERVER_USE:
    # Set GPU number to use
    os.environ["CUDA_VISIBLE_DEVICES"] = _LAB_SERVER_USE_GPU_NUM

# W_in : torch.tensor (V, D)
# W_out : torch.tensor (OH, D)
W_in = load(_W_IN_FILENAME).cuda()
W_out = load(_W_OUT_FILENAME).cuda()
V, D = W_in.size()
OH, D2 = W_out.size()

if D != D2:
    print('Invalid W_in, W_out size.')
    print('W_in size : ' + str(V) + ' ' + str(D))
    print('W_out size : ' + str(OH) + ' ' + str(D2))
    exit(0)


def classify(inputvec):
    # inputvec : torch.tensor(1, V)
    # output : torch.tensor(1, OH)
    return inputvec.mm(W_in).mm(W_out.t())


def pick_top_n(outputvec, n):
    # outputvec : torch.tensor(1, OH)
    # n : int (it must satisfy (0 < n <= OH))
    # output : int list
    # output : index of top n values in outputvec.
    #   e.g. pick_top_n(tensor([[1.0, 3.0, 2.0, 4.0]]), 2) --> [3, 1]
    #   The case where two or more elements have the same value is not considered.

    l = [a.item() for a in outputvec.flatten()]
    return [l.index(k) for k in sorted(l, reverse=True)[:n]]


def test_so_one_content(filename, n):
    # filename : string. a filename from datasearch.obj3_getfilelist() or datasearch.obj3_allfilelist()
    # n : int. pick top n candidate answers.

    # correct : int. the number of corrrect candidate answers.
    # candidates : int list. what leraning results infer from content.
    # answerurls : int list. the correct answers.

    # read file
    tailfilename = obj3_getdistinctfilename(filename)
    contentstr, answerurls = obj3_readfile(filename, isupperpydocused=True)
    contentstr = tailfilename + ' ' + contentstr

    # construct input vector.
    ws = str2unigramhashlist(contentstr, _HASH_BIT_SIZE)
    inputvec = torch.zeros(1, V).cuda()
    ov = torch.zeros(1, OH).cuda()
    for h in ws:
        inputvec = torch.zeros(1, V).cuda()
        inputvec[0][h] = 1.0
        ov += classify(inputvec) / len(ws)
        inputvec[0][h] = 0.0

    candidates = pick_top_n(ov, n)

    # count correct answers.
    # https://stackoverflow.com/a/15375122
    correct = sum(1 for i in candidates if i in answerurls)

    return correct, candidates, answerurls


def test_query(s, candidate_num=_N_FOR_TOP_N_VALUES, answers=None, stdoutprint=True, outputfiledescriptor=None):
    ws = str2unigramhashlist(s, _HASH_BIT_SIZE)
    ov = torch.zeros(1, OH).cuda()
    for h in ws:
        inputvec = torch.zeros(1, V).cuda()
        inputvec[0][h] = 1.0
        ov += classify(inputvec)
    ca = pick_top_n(ov, candidate_num)

    if stdoutprint:
        print('QUERY:')
        print('\t' + s)
        print('CANDIDATES:')
        for c in ca:
            print('\t' + num2upperpydoc[c])
        if answers is not None:
            print('ANSWERS:')
            for a in answers:
                print('\t' + num2upperpydoc[a])
            correctcount = sum(1 for i in ca if i in answers)
            print('CORRECT: ' + str(correctcount) + ' / ' + str(len(answers)))
        print('')
        sys.stdout.flush()
    elif outputfiledescriptor is not None:
        outputfiledescriptor.write('QUERY:\n')
        outputfiledescriptor.write('\t' + s + '\n')
        outputfiledescriptor.write('CANDIDATES:' + '\n')
        for c in ca:
            outputfiledescriptor.write('\t' + num2upperpydoc[c] + '\n')
        if answers is not None:
            outputfiledescriptor.write('ANSWERS:\n')
            for a in answers:
                outputfiledescriptor.write('\t' + num2upperpydoc[a] + '\n')
            correctcount = sum(1 for i in ca if i in answers)
            outputfiledescriptor.write(
                'CORRECT: ' + str(correctcount) + ' / ' + str(len(answers)) + '\n\n')


def test_so_N_contents(N=_N_FOR_TESTCASE_NUM, candidate_num=_N_FOR_TOP_N_VALUES, logging=True, specific_logging=True, random=False):
    # N : int. the number of contents to test. if N <= 0, this will test for whole contents.
    # candidate_num : int. it is for the argument value for pick_top_n function. (it must satisfy (0 < n <= OH))
    # logging : bool. True for printing two-line result of test_so_one_content(). (question name, the number of correct answers / total correct answers)
    # specific_logging : bool. True for printing the whole results of test_so_one_content(). (including the name of answers.)
    # random : bool. True for selecting N testcases randomly. Otherwise, it will test N contents from the front of the datasearch.obj3_allfilelist().

    # corrects : int list.
    # candidates : int list list.
    # answerurls : int list list.

    allfilenames = obj3_allfilelist()
    corrects = []
    candidates = []
    answerurls = []
    answercount = 0

    with open(_RESULT_LOG_FILENAME, 'w') as logfile:
        iter_count = 0
        for fn in allfilenames:
            iter_count += 1
            if N > 0 and iter_count > N:
                break

            co, ca, an = test_so_one_content(fn, candidate_num)
            corrects.append(co)
            candidates.append(ca)
            answerurls.append(an)
            answercount += len(an)

            if logging:
                fntail = obj3_getdistinctfilename(fn)
                logfile.write('ITEATION ' + str(iter_count) + ' =>\tCORRECT: ' + str(
                    co) + ' / ' + str(len(an)) + '\t\tFILE: ' + fntail + '\n')
            if specific_logging:
                logfile.write('CANDIDATES:\n')
                for c in ca:
                    logfile.write('\t' + num2upperpydoc[c] + '\n')
                logfile.write('ANSWERS:\n')
                for a in an:
                    logfile.write('\t' + num2upperpydoc[a] + '\n')
            if logging or specific_logging:
                logfile.write('\n')

        if logging or specific_logging:
            logfile.write('TOTAL CORRECT: ' + str(sum(corrects)
                                                  ) + ' / ' + str(answercount) + '\n')

    return corrects, candidates, answerurls


if not _DEBUG_MODE:
    test_so_N_contents()

with open(_RESULT_LOG_FILENAME, 'w') as logfile:
    for fn in obj3_allfilelist():
        s = obj3_getdistinctfilename(fn)
        _, a = obj3_readfile(fn, isupperpydocused=True)
        test_query(s, candidate_num=5, answers=a, stdoutprint=False, outputfiledescriptor=logfile)
