import numpy as np

# Constants
fixed_point = 8


def encrypt_nparray(nparray: np.array):
    """
    加密numpy数组
    """
    nparray = (nparray * (10 ** fixed_point)).astype(np.int64)
    print(nparray)
