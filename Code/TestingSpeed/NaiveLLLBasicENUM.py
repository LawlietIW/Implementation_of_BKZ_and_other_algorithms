import sys
import os
import time 
import numpy as np


# Get the absolute path of ParentFolder
parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Navigate one level up from A
# Add ParentFolder to the Python path
sys.path.append(parent_folder_path)

from TestingSpeed.UltimateBKZ import ultimate_BKZ
from BKZ_first_implementation.galbraithLLL import Galbraith_LLL_removing_linear_dependence
from BKZ_first_implementation.enumeration import enum_short_vector
from BetterImplementation.Knutsfix import improvedLLL
from BetterImplementation.schnorr_enumeration import Schnorr_ENUM

Bm = np.array([[33,89,18,17,30],
 [ 3,42,93,48,26],
 [17, 4,67,63,74],
 [55,36,77,92,17],
 [34,36,70, 9,84]])


print("Bm")
print(np.array2string(Bm,separator=','))
start = time.time()
BKZBm = ultimate_BKZ(Bm, improvedLLL, Schnorr_ENUM, delta = 0.8, beta = 3)
print("Time taken: ", time.time() - start)
print()
print("BKZBm")
print(np.array2string(BKZBm,separator=','))