import string

_ALPHA_NUM_WS = string.ascii_letters + string.digits + string.whitespace

def make_subword(w, lowlength, highlength):
    # w : string
    # OUTPUT : string list. subword list of w. subword's length is [lowlength, highlength]

    # refer https://stackoverflow.com/a/6934201
    return [w[i:j] for i in range(len(w)) for j in range(i + lowlength, i + highlength + 1)]


def alphanumws_converter(c, replace=' '):
    # c : character (length-1 string)
    
    # Examples (when replace=' ')
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
