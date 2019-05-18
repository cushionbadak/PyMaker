import string

_ALPHA_NUM_WS = string.ascii_letters + string.digits + string.whitespace


def alphanumws_converter(c, replace=' '):
    # c : character (length-1 string)

    # Examples :
    #   alphanumws_converter('a') => 'a'
    #   alphanumws_converter('\n') => '\n'
    #   alphanumws_converter('2') => '2'
    #   alphanumws_converter(' ') => ' '
    #   alphanumws_converter('_') => ' '
    return c if c in _ALPHA_NUM_WS else replace


def formatsplit(s):
    # s : string (whole bunch of contents)
    # output : string list

    # Example using alphanumws_converter :
    #   formatsplit('as3 ][3i] z-12 p.pow')
    #   => ['as3', '3i', 'z', '12', 'p', 'pow']

    # To change its' behavior, you should change alphanumws_converter to other function.
    return ''.join(list(map(alphanumws_converter, s))).split()


def stringhash(s, hash_bit_size):
    # input : string
    # output : int between [0, (2 ** HASH_BIT_SIZE) - 1]
    return hash(s) & ((1 << hash_bit_size) - 1)


def bigramhash(w1, w2, hash_bit_size, concatstr=' '):
    # w1 : string
    # w2 : string
    # output : int between [0, (2 ** HASH_BIT_SIZE) - 1]
    return stringhash(w1 + concatstr + w2, hash_bit_size)


def bigramhashlist(word_seq, hash_bit_size):
    # word_seq : string list (string length should be greater than 1)
    # output : int list (list of hashed bigram)
    return [bigramhash(word_seq[i-1], word_seq[i], hash_bit_size, concatstr=' ') for i in range(1, len(word_seq))]


def unigramhashlist(word_seq, hash_bit_size):
    return [stringhash(w, hash_bit_size) for w in word_seq]


def str2bigramhashlist(s, hash_bit_size=20):
    # s : string (long string)
    # output : int list (list of hashed bigram)
    return bigramhashlist(formatsplit(s), hash_bit_size)


def str2unigramhashlist(s, hash_bit_size=20):
    return unigramhashlist(formatsplit(s), hash_bit_size)