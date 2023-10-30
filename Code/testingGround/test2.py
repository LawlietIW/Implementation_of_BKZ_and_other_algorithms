import numpy as np
from betterUtils import *

Bm = np.array([[  4, -31, -25],
 [ 38,  30,  -5],
 [ 22,  83,  47]])


B_gs, Mym = gram_schmidt(Bm)

print(Mym)
print(B_gs)