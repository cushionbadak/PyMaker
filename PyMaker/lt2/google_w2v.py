# refer: http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/

import gensim

print('google_w2v.py: import google w2v model...')
model = gensim.models.Word2Vec.load_word2vec_format(
    '../datas/GoogleNews/GoogleNews-vectors-negative300/bin', binary=True)
print('google_w2v.py: finish importing google w2v model.')

def unigram_sentence_wordvecsum(ws):
    # ws : string list. this word list should be longer than 0.
    if len(ws) < 1:
        return None
    initv = model.wv[ws[0]]
    initv -= initv  # make initv zero.
    for w in ws:
        initv += model.wv[w]

