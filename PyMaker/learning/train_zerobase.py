import os
import sys
import torch
from torch.serialization import save
from torch.serialization import load
import string

from datasearch import *
from stringhash import str2bigramhashlist


# No pre-trained word embedding
# No negative sampling.
# No subsampling.
# Use hash value to get the index of the word.

# Constants and Hyperparameters
_C = {}
_C['DEBUG_MODE'] = False
_C['LAB_SERVER_USE'] = True
_C['LAB_SERVER_USE_GPU_NUM'] = "03"
# If ITER_COUNT_DEBUG_INFO_PERIOD <= 0, program will not print losses.
_C['ITER_COUNT_DEBUG_INFO_PERIOD'] = 2000
# If TRAIN_CONTENTNUM_UPPER_LIMIT <= 0, program will learn for the whole training set.
_C['TRAIN_CONTENTNUM_UPPER_LIMIT'] = 0

_C['HASH_BIT_SIZE'] = 20
_C['DIMENSION'] = 64
_C['LEARNING_RATE'] = 0.01

_C['W_IN_FILENAME'] = 'zerobase_learned_w_in.pt'
_C['W_OUT_FILENAME'] = 'zerobase_learned_w_out.pt'


def print_constants_to_str():
    # input : void
    # output : string s
    s = ''
    for key in _C:
        s += str(key) + '\t: ' + str(_C[key]) + '\n'
    return s


def get_gradient(input_hash, output_class, W_in, W_out):
    # input_hash : int
    # output_class : int. It should be the value between [0, K], the value K is from the W_out's shape.
    # W_in : torch.tensor((2 ** HASH_BIT_SIZE), D)
    # W_out : torch.tensor(K, D)

    # loss : torch.tensor(1)
    # grad_in : torch.tensor(1, D)
    # grad_out : torch.tensor(K, D)

    _, D = W_in.size()
    inputVector = W_in[input_hash]
    out = W_out.mm(inputVector.view(D, 1))

    expout = torch.exp(out)
    softmax = expout / expout.sum()
    loss = -torch.log(softmax[output_class])

    grad = softmax
    grad[output_class] -= 1.0

    grad_in = grad.view(1, -1).mm(W_out)
    grad_out = grad.mm(inputVector.view(1, -1))

    return loss, grad_in, grad_out


def train_one_content(input_string, output_classes, W_in, W_out, learning_rate=_C['LEARNING_RATE']):
    # INPUTS
    # input_string : string (all content)
    # output_classes : int list. Each of them should be the value between [0, K], the value K is from the W_out's shape.
    # W_in : torch.tensor((2 ** HASH_BIT_SIZE), D)
    # W_out : torch.tensor(K, D)

    # OUTPUTS
    # avg_loss : float. average loss recordecd while learning.
    # W_in (learned)
    # W_out (learned)

    losses = []
    inputhashlist = str2bigramhashlist(input_string)
    # print('PROFILING INFO : len(output_classes) * len(inputhashlist) = ' +
    #      str(len(output_classes) * len(inputhashlist)))
    for output_class in output_classes:
        for h in inputhashlist:
            L, G_in, G_out = get_gradient(h, output_class, W_in, W_out)
            # I don't know why squeeze method needed, but I don't test whether it works well when squeeze method does not exist.
            losses.append(L.item())
            W_in[h] -= learning_rate * G_in.squeeze()
            W_out -= learning_rate * G_out

    avg_loss = 0
    if len(losses) != 0:
        avg_loss = sum(losses) / len(losses)

    return avg_loss, W_in, W_out


def main():
    # GPU setting
    if _C['LAB_SERVER_USE']:
        # Set GPU number to use
        os.environ["CUDA_VISIBLE_DEVICES"] = _C['LAB_SERVER_USE_GPU_NUM']

    dimension = _C['DIMENSION']
    iter_count_debug_info_period = _C['ITER_COUNT_DEBUG_INFO_PERIOD']

    print(print_constants_to_str())

    # Xavier initialization of weight matrices
    W_in = torch.randn((1 << _C['HASH_BIT_SIZE']),
                       dimension).cuda() / (dimension**0.5)
    W_out = torch.randn(len(num2pydoc), dimension).cuda() / (dimension**0.5)

    # LEARNING
    print('Collect all training filenames.')
    obj3_filenamelist = obj3_allfilelist()
    iter_count = 0
    avglosses = []
    print('Training Start.')
    for filename in obj3_filenamelist:
        iter_count += 1
        if _C['TRAIN_CONTENTNUM_UPPER_LIMIT'] > 0 and _C['TRAIN_CONTENTNUM_UPPER_LIMIT'] < iter_count:
            break

        content, answers = obj3_readfile(filename)

        # train title
        _, lastfilename = os.path.split(filename)
        _, W_in, W_out = train_one_content(
            lastfilename, answers, W_in, W_out, learning_rate=_C['LEARNING_RATE'])

        # train content
        avgloss, W_in, W_out = train_one_content(
            content, answers, W_in, W_out, learning_rate=_C['LEARNING_RATE'])

        avglosses.append(avgloss)
        if (iter_count_debug_info_period > 0) and (iter_count % iter_count_debug_info_period == 0):
            print("Content Iteration : " + str(iter_count))
            if len(avglosses) != 0:
                print("LOSS : %f" % (sum(avglosses)/len(avglosses),))
            else:
                print("LOSS : N/A")
            avglosses = []

        sys.stdout.flush()

    # SAVE W_in W_out to file.
    save(W_in, _C['W_IN_FILENAME'])
    save(W_out, _C['W_OUT_FILENAME'])


if not _C['DEBUG_MODE']:
    main()
