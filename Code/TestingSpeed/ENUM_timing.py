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

from BKZ_first_implementation.utils.utilFunctions import gram_schmidt, calc_norm




############################################
############### FUNCTIONS ##################
############################################


 
def format_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes)} minutes, {int(remaining_seconds)} seconds"


def which_BKZ_to_use(check):
    #Ugly but I want the same structure as in the other file
    if check == "NN":
        """NN = NaiveENUM"""
        latex_path = 'TestingSpeed/Timing/NL_NE/ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/NL_NE/ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/Timing/NL_NE/BKZ_of_test_matrices.json'
    elif check == "NI":
        """NI = NaiveLLLImprovedENUM"""
        latex_path = 'TestingSpeed/Timing/NL_IE/ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/NL_IE/ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/Timing/NL_IE/BKZ_of_test_matrices.json'
    elif check == "IN":
        """IN = ImprovedLLLNaiveENUM"""
        latex_path = 'TestingSpeed/IL_NE/ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/IL_NE/ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/IL_NE/BKZ_of_test_matrices.json'
    elif check == "II":
        """II = ImprovedLLLImprovedENUM"""
        latex_path = 'TestingSpeed/Timing/IL_IE/ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/IL_IE/ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/Timing/IL_IE/BKZ_of_test_matrices.json'
    elif check == "Sage":
        """Sage = SAGEMATH_BKZ"""
        latex_path = 'TestingSpeed/Timing/Sage/ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/Sage/ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/Timing/Sage/BKZ_of_test_matrices.json'
    elif check == "Test_naive":
        """Test = we just test on the test_file. """
        latex_path = 'TestingSpeed/Timing/Test_times/naive_ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/Test_times/naive_ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/test_files/test_matrices_for_naive_LLL.json'
    elif check == "Test_improved":
        """Test = we just test on the test_file.    """
        latex_path = 'TestingSpeed/Timing/Test_times/improved_ENUM_times_latex.csv'
        readable_path = 'TestingSpeed/Timing/Test_times/improved_ENUM_times_readable.csv'
        BKZ_path = 'TestingSpeed/test_files/test_matrices_for_improved_LLL.json'
    else:
        print("You have to choose between NN, NI, IN, II, Sage, Test_naive, Test_improved")
        assert(False)
    return latex_path, readable_path, BKZ_path



def measure_time(BKZm, ENUM):
    BKZ_gs, Mym = gram_schmidt(BKZm)
    BKZ_norms = calc_norm(BKZ_gs)
    start_time = time.time()
    a, b_, c_bar = ENUM(BKZm, Mym, BKZ_norms)
    end_time = time.time()
    execution_time = end_time - start_time
    return b_,c_bar, execution_time

# Function to save a list of matrices to a JSON file
# def write_matrices_to_json(file_name, matrices):
#     with open(file_name, 'w') as json_file:
#         json.dump(matrices, json_file)

# Function to read the list of matrices from a JSON file
def read_matrices_from_json(file_name):
    with open(file_name, 'r') as json_file:
        matrices = json.load(json_file)
        return matrices

















############################################
############### VARIABLES ##################
############################################

WHAT_TO_TEST = "NI"  #NN, NI, IN, II', 'Sage', 'Test_naive', 'Test_improved'

ENUM = Improved_ENUM


HARD_N = 50




############################################
############# LETS START TIMING ############
############################################




latex_path, readable_path, BKZ_path = which_BKZ_to_use(WHAT_TO_TEST)
list_of_BKZ = read_matrices_from_json(BKZ_path)

timing_results = []


for BKZm in tqdm(list_of_BKZ):
    BKZm = np.array(BKZm)   #make it back into array
    # print("Working on next")
    b_,c_bar, exec_time = measure_time(BKZm, ENUM)
    # list_of_BKZ.append(result.tolist())  #got to be a list to save in json
    current_n = BKZm.shape[0]

    timing_results.append({
        'n': current_n,
        'Length (int)': int(c_bar),
        'Time (s)': f"{exec_time:.6f}",
        'Readable Time': format_seconds(exec_time),
        # 'Shortest_vector': b_
    })

    if current_n >= HARD_N:
        ### I just want the data to be saved even though it starts taking a long time
        df = pd.DataFrame(timing_results)
        df.to_csv(latex_path, sep='&', index=False)
        df.to_csv(readable_path, sep=',', index=False)


# Create a DataFrame from the results
df = pd.DataFrame(timing_results)
# Write the DataFrame to an Excel file
df.to_csv(latex_path, sep='&', index=False)
df.to_csv(readable_path, sep=',', index=False)





############################################
############# LETS PRINT RESULTS ###########
############################################




print(df)
dict_to_view_methods = {
    "NN": ["Naive", "Naive"],
    "NI": ["Naive", "Improved"],
    "IN": ["Improved", "Naive"],
    "II": ["Improved", "Improved"],
    "Sage": ["Sage", "Sage"],
    "Test_naive": ["test_file_naive", "x"],
    "Test_improved": ["test_file_improved", "x"],
}

LLLname = dict_to_view_methods[WHAT_TO_TEST][0]
ENUMname = dict_to_view_methods[WHAT_TO_TEST][1]

if ENUM.__name__ == "enum_short_vector":
    EnumerationMethodForTiming = "Naive"
elif ENUM.__name__ == "Schnorr_ENUM":
    EnumerationMethodForTiming = "Improved"

print("----------------------------------------")
print()
print("We have tested enumeration on the following:")
print("BKZ_LLL: ", LLLname)
print("BKZ_ENUM: ", ENUMname)
print()
print("By using enumeration:")
print(EnumerationMethodForTiming)