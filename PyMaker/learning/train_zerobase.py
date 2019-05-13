import torch
import string

from stringhash import str2bigramhashlist

# No pre-trained word embedding
# No negative sampling.
# No subsampling.
# Use hash value to get the index of the word.

# Constants and Hyperparameters
_C = {}
_C['HASH_BIT_SIZE'] = 20
_C['DEBUG_MODE'] = True
_C['LEARNING_RATE'] = 0.01


def print_constants_to_str():
    # input : void
    # output : string s
    s = ''
    for key in _C:
        s += str(key) + '\t:' + str(_C[key]) + '\n'
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
    for output_class in output_classes:
        for h in inputhashlist:
            L, G_in, G_out = get_gradient(h, output_class, W_in, W_out)
            losses.append()
            # I don't know why squeeze method needed, but I don't test whether it works well when squeeze method does not exist.
            W_in[h] -= learning_rate * G_in.squeeze()
            W_out -= learning_rate * G_out
            losses.append(L.item())

    avg_loss = sum(losses) / len(losses)
    return avg_loss, W_in, W_out


def main():
    # TODO
    pass


if not _C['DEBUG_MODE']:
    main()
