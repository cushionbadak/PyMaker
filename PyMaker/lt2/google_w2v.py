# refer: http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/

import gensim
import numpy as np

print('google_w2v.py: import google w2v model...')
print('google_w2v.py: it will take about 2 minutes and over 2GB of memory needed to load.')
model = gensim.models.KeyedVectors.load_word2vec_format(
    'PyMaker/datas/GoogleNews/GoogleNews-vectors-negative300.bin', binary=True)
print('google_w2v.py: finish importing google w2v model.')

def unigram_sentence_wordvecsum(ws):
    # ws : string list. this word list should be longer than 0.
    if len(ws) < 1:
        return None

    for w in ws:
        # make initv zero value.
        if w in model:
            initv = np.copy(model[w])
            initv -= initv
    for w in ws:
        if w in model:
            initv += model[w]

    return initv
