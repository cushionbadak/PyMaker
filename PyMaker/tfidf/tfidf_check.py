# Notice
# Before run this, you need to turn off tfidf_g.py 's OBJ4_WC_RUN to False and turn on OBJ4_WC_TOTAL_LOAD to True.

import pickle

# import modules from sibling directory.
# https://stackoverflow.com/a/9806045
# https://stackoverflow.com/a/27876800
import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import obj4_countwords
import tfidf_g
from t3.obj4_read import *

checkresultfilepath = 'PyMaker/tfidf/check/'
checkresultfilename = checkresultfilepath + 'result2.txt'

dfc = obj4_countwords.obj4_dfc
dfcsum = obj4_countwords.dfcsum

df = {k: (v/dfcsum) for k, v in dfc.items()}

with open (checkresultfilename, 'w') as f:
    for i in range(tfidf_g.OBJ4_SIZE):
        l, _ = obj4_str(obj4_filename(i, includepath=True))
        tfcsum, tfc = obj4_countwords.load_obj4_tfc(i)
        tf = {k : (v / tfcsum) for k, v in tfc.items()}
        f.write('\n\nFile ' + str(i) + '\t' + l + '\n')
        for k, v in tf.items():
            f.write('\t' + k + ' : ' + str(obj4_countwords.tfidf(v, df[k], 1.5)) + '\n')