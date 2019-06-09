OBJ4_SIZE = 10655

DATAPATH = 'PyMaker/datas/'
OBJ4_VECREP_PATH = DATAPATH + 'object4_tfidf_sw_vecrep/'

## obj4_countwords.py specific
OBJ4_WC_RUN = False
OBJ4_WC_TOTAL_LOAD = True

OBJ4_WC_PATH = DATAPATH + 'obj4_wc/'
OBJ4_WC_TOTALCOUNT_DICT_FILENAME = OBJ4_WC_PATH + 'totaldict.txt'
OBJ4_WC_DOCCOUNT_DICT_FILENAME_PREFIX = OBJ4_WC_PATH + 'docdict_'
OBJ4_WC_DOCCOUNT_DICT_FILENAME_POSTFIX = '.txt'

def obj4_wc_doccount_dict_filename(n):
    # n : int
    # example : 1 => 'PyMaker/datas/obj4_wc/docdict_1.txt'
    return OBJ4_WC_DOCCOUNT_DICT_FILENAME_PREFIX + str(n) + OBJ4_WC_DOCCOUNT_DICT_FILENAME_POSTFIX


## obj4_vecrep_calc.py specific
OBJ4_VECREP_CALC_SAVE_DOCVEC_PRINT_LOG = True
OBJ4_VECREP_CALC_SET_GLOBAL_VARIABLES = True
OBJ4_VECREP_CALC_SET_GLOBAL_VARIABLES_PRINT_LOG = True
OBJ4_VECREP_CALC_ALLOW_PICKLE = False
SUBWORD_LENGTH_LOW = 3
SUBWORD_LENGTH_HIGH = 6
OBJ4_VECREP_CALC_ALLOW_PICKLE = False

def tfidf_obj4_vecrep_filename(n, includepath=True):
    # output : string. (pathname depends on t3_global.OBJ4_VECREP_PATH)
    # example : obj4_vecrep_filename(3, True) => 'PyMaker/datas/object4_subword_vecrep/3'
    # when you save numpy array to file, numpy automatically appends '.npy' at the end of the filename.
    # when you load file to numpy array, you need to append '.npy' to the filename manually.
    return (OBJ4_VECREP_PATH if includepath else '') + str(n)

