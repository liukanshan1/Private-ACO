import numpy as np

from ss.secret import Secret

# Constants
fixed_point = 8
encrypted = True


def encrypt_nparray(nparray: np.array):
    """
    加密numpy数组
    """
    nparray = (nparray * (10 ** fixed_point)).astype(np.int64)
    e_nparray = np.empty(nparray.shape, dtype=Secret, order='C')
    for i in range(nparray.shape[0]):
        for j in range(nparray.shape[1]):
            e_nparray[i, j] = Secret(nparray[i, j])
    return e_nparray


def get_fixed_point():
    return fixed_point

def get_if_encrypted():
    return encrypted
