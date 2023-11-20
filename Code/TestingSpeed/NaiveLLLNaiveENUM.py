import sys
import os
import time 
import numpy as np
import pandas as pd

# Get the absolute path of ParentFolder
parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Navigate one level up from A
# Add ParentFolder to the Python path
sys.path.append(parent_folder_path)

from TestingSpeed.UltimateBKZ import ultimate_BKZ
from BKZ_first_implementation.galbraithLLL import Galbraith_LLL_removing_linear_dependence as Naive_LLL
from BKZ_first_implementation.enumeration import enum_short_vector as Naive_ENUM
from BetterImplementation.Knutsfix import improvedLLL as Improved_LLL
from BetterImplementation.schnorr_enumeration import Schnorr_ENUM as Improved_ENUM

############################################
############### FUNCTIONS ##################
############################################


def make_Bm_from_n_list(n_list, max_number):
    list_of_Bm = []
    for n in n_list:
        Bm = np.random.randint(max_number, size=(n,n))
        list_of_Bm.append(Bm)
    return list_of_Bm
 

# list_of_Bm = [
# np.array([[33,89,18,17,30],
#  [ 3,42,93,48,26],
#  [17, 4,67,63,74],
#  [55,36,77,92,17],
#  [34,36,70, 9,84]]),
#  np.array([[33,89,18,17,30],
#  [ 3,42,93,48,26],
#  [17, 4,67,63,74],
#  [55,36,77,92,17],
#  [34,36,70, 9,84]])]

def measure_time(Bm, delta, beta):
    start_time = time.time()
    result = ultimate_BKZ(Bm, Naive_LLL, Naive_ENUM, delta = delta, beta = beta)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def format_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes} minutes, {int(remaining_seconds)} seconds"




############################################
############# LETS START TIMING ############
############################################


n_list = [20,30,40,50,60]
MAX_NUMBER = 500
delta = 0.8
beta = 3

list_of_Bm = make_Bm_from_n_list(n_list, MAX_NUMBER) 


timing_results = []


for Bm in list_of_Bm:
    print("Working on next")
    result, exec_time = measure_time(Bm, delta, beta)
    current_n = Bm.shape[0]

    timing_results.append({
        'n': current_n,
        'Delta': delta,
        'Beta': beta,
        'Max number' : MAX_NUMBER,
        'Time (s)': f"{exec_time:.6f}",
        'Readable Time': format_seconds(exec_time)
    })

    if current_n > 80:
        ### I just want the data to be saved even though it starts taking a long time
        df = pd.DataFrame(timing_results)
        df.to_csv('TestingSpeed/NL_NE/NaiveLLLNaiveENUM_latex.csv', sep='&', index=False)
        df.to_csv('TestingSpeed/NL_NE/NaiveLLLNaiveENUM_readable.csv', sep=',', index=False)


# Create a DataFrame from the results
print("Print to Excel")
df = pd.DataFrame(timing_results)

print(df)
# Write the DataFrame to an Excel file
df.to_csv('TestingSpeed/NL_NE/NaiveLLLNaiveENUM_latex.csv', sep='&', index=False)
df.to_csv('TestingSpeed/NL_NE/NaiveLLLNaiveENUM_readable.csv', sep=',', index=False)





# print("Bm")
# print(np.array2string(Bm,separator=','))
# start = time.time()
# BKZBm = ultimate_BKZ(Bm, improvedLLL, Schnorr_ENUM, delta = 0.8, beta = 3)
# print("Time taken: ", time.time() - start)
# print()
# print("BKZBm")
# print(np.array2string(BKZBm,separator=','))