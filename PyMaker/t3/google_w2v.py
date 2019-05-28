# refer: http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/

import gensim
import numpy as np

from . import t3_global

# initialize
model = 0
vecrepLength = 0


if t3_global.GOOGLE_W2V_SET_GLOBAL_VARIABLES:
    if t3_global.GOOGLE_W2V_SET_GLOBAL_VARIABLES_PRINT_LOG:
        print('google_w2v.py: import google w2v model...')
        print('google_w2v.py: it will take about 2 minutes and over 2GB of memory needed to load.')

    model = gensim.models.KeyedVectors.load_word2vec_format(t3_global.GOOGLE_W2V_PATH, binary=True)
    vecrepLength = len(model['car'])

    if t3_global.GOOGLE_W2V_SET_GLOBAL_VARIABLES_PRINT_LOG:
        print('google_w2v.py: finish importing google w2v model.')


# << GENERAL NOTICE >>
# If w2v model cannot make any representation for given input,
# it will return near-zero vector (one-hot vector with the value t3_global.GOOGLE_W2V_NEAR_ZERO).
def zerovector():
    return np.zeros(vecrepLength)


def make_nzv(v):
    # make near-zero-vector from zerovector v.
    # If arg v does not changed, this code should be modified.
    v[np.random.randint(low=0, high=vecrepLength)] += t3_global.GOOGLE_W2V_NEAR_ZERO
    return


def unigram_sentence_wordvecsum(ws):
    # ws : string list.
    # OUTPUT : numpy array
    initv = zerovector
    for w in ws:
        if w in model:
            initv += model[w]
    
    # https://stackoverflow.com/a/23567941/10353572
    if not np.any(initv):
        make_nzv(initv)

    return initv


def subword_sentence_wordvecsum(ws):
    # ws : string list.
    # slicing word into subwords (subword length is defined at t3_global)
    initv