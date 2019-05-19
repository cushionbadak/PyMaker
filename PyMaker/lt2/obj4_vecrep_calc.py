from numpy import save

from lt2_global import *
from obj4_read import *
from google_w2v import *

fns = obj4_allfilename()
for i in range(0, 10655):
    _, c = obj4_str(obj4_filename(i, includepath=True))
    ofilename = obj4_vecrep_filename(i)
    save(ofilename, unigram_sentence_wordvecsum(c))

