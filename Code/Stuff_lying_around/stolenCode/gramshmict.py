# L-20 MCS 507 Fri 11 Oct 2013 : gramschmidt.py

"""
Given pseudo code for the Gram-Schmidt method,
define Python code.
"""

import numpy as np

def gramschmidt(A):
    """
    Applies the Gram-Schmidt method to A
    and returns Q and R, so Q*R = A.
    """
    R = np.zeros((A.shape[1], A.shape[1]))
    Q = np.zeros(A.shape)
    for k in range(0, A.shape[1]):
        R[k, k] = np.sqrt(np.dot(A[:, k], A[:, k]))
        Q[:, k] = A[:, k]/R[k, k]
        for j in range(k+1, A.shape[1]):
            R[k, j] = np.dot(Q[:, k], A[:, j])
            A[:, j] = A[:, j] - R[k, j]*Q[:, k]
    return Q, R

a = gramschmidt(np.array(
    [[  9,  -8,   8,  -4],
    [  2,  15,  12,   9],
    [ -7 , -6  ,10 , 16],
    [ 14 ,  2, -18 , 10]]))


print(a[0])