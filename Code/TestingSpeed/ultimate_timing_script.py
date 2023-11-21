import sys
import os
import time 
import numpy as np
import pandas as pd
from tqdm import tqdm
import json

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




 
def format_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes)} minutes, {int(remaining_seconds)} seconds"


def what_to_test(check):
    if check == "NN":
        """NN = NaiveLLLNaiveENUM"""
        latex_path = 'TestingSpeed/NL_NE/NaiveLLLNaiveENUM_latex.csv'
        readable_path = 'TestingSpeed/NL_NE/NaiveLLLNaiveENUM_readable.csv'
        BKZ_path = 'TestingSpeed/NL_NE/BKZ_of_test_matrices.json'
        LLL = Naive_LLL
        ENUM = Naive_ENUM
    if check == "NI":
        """NI = NaiveLLLImprovedENUM"""
        latex_path = 'TestingSpeed/NL_IE/NaiveLLLImprovedENUM_latex.csv'
        readable_path = 'TestingSpeed/NL_IE/NaiveLLLImprovedENUM_readable.csv'
        BKZ_path = 'TestingSpeed/NL_IE/BKZ_of_test_matrices.json'
        LLL = Naive_LLL
        ENUM = Improved_ENUM
    if check == "IN":
        """IN = ImprovedLLLNaiveENUM"""
        latex_path = 'TestingSpeed/IL_NE/ImprovedLLLNaiveENUM_latex.csv'
        readable_path = 'TestingSpeed/IL_NE/ImprovedLLLNaiveENUM_readable.csv'
        BKZ_path = 'TestingSpeed/IL_NE/BKZ_of_test_matrices.json'
        LLL = Improved_LLL
        ENUM = Naive_ENUM
    if check == "II":
        """II = ImprovedLLLImprovedENUM"""
        latex_path = 'TestingSpeed/IL_IE/ImprovedLLLImprovedENUM_latex.csv'
        readable_path = 'TestingSpeed/IL_IE/ImprovedLLLImprovedENUM_readable.csv' 
        BKZ_path = 'TestingSpeed/IL_IE/BKZ_of_test_matrices.json'
        LLL = Improved_LLL
        ENUM = Improved_ENUM
    return LLL,ENUM, latex_path, readable_path, BKZ_path



def measure_time(Bm, delta, beta, LLL, ENUM):
    start_time = time.time()
    result = ultimate_BKZ(Bm, LLL, ENUM, delta = delta, beta = beta)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Function to save a list of matrices to a JSON file
def write_matrices_to_json(file_name, matrices):
    with open(file_name, 'w') as json_file:
        json.dump(matrices, json_file)

# Function to read the list of matrices from a JSON file
def read_matrices_from_json(file_name):
    with open(file_name, 'r') as json_file:
        matrices = json.load(json_file)
        return matrices

############################################
############### VARIABLES ##################
############################################

WHAT_TO_TEST = "IN"  #NN, NI, IN, II

delta = 0.8
beta = 3

HARD_N = 50  #When do we want to print to file every step, cause every step takes so much time



list_of_Bm = read_matrices_from_json("TestingSpeed/test_matrices.json") 
list_of_BKZ = []
############################################
############# LETS START TIMING ############
############################################

LLL,ENUM, latex_path, readable_path, BKZ_path = what_to_test(WHAT_TO_TEST)

timing_results = []


for Bm in tqdm(list_of_Bm):
    Bm = np.array(Bm)   #make it back into array
    max_number = np.amax(Bm)
    # print("Working on next")
    result, exec_time = measure_time(Bm, delta, beta,  LLL, ENUM)
    list_of_BKZ.append(result.tolist())  #got to be a list to save in json
    current_n = Bm.shape[0]

    timing_results.append({
        'n': current_n,
        'Delta': delta,
        'Beta': beta,
        'Max number' : max_number,
        'Time (s)': f"{exec_time:.6f}",
        'Readable Time': format_seconds(exec_time)
    })

    if current_n > HARD_N:
        ### I just want the data to be saved even though it starts taking a long time
        df = pd.DataFrame(timing_results)
        df.to_csv(latex_path, sep='&', index=False)
        df.to_csv(readable_path, sep=',', index=False)


# Create a DataFrame from the results
print("Print to Excel")
df = pd.DataFrame(timing_results)

print(df)
# Write the DataFrame to an Excel file
df.to_csv(latex_path, sep='&', index=False)
df.to_csv(readable_path, sep=',', index=False)
write_matrices_to_json(BKZ_path, list_of_BKZ)





# print("Bm")
# print(np.array2string(Bm,separator=','))
# start = time.time()
# BKZBm = ultimate_BKZ(Bm, improvedLLL, Schnorr_ENUM, delta = 0.8, beta = 3)
# print("Time taken: ", time.time() - start)
# print()
# print("BKZBm")
# print(np.array2string(BKZBm,separator=','))