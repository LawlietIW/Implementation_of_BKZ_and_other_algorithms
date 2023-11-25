import numpy as np
import json

# Function to make a list of matrices
def make_Bm_from_n_list(n_list, max_number):
    list_of_Bm = []
    for n in n_list:
        Bm = np.random.randint(max_number, size=(n,n))
        list_of_Bm.append(Bm.tolist())  #got to be a list to save in json
    return list_of_Bm

def write_matrices_to_json(file_name, matrices):
    with open(file_name, 'w') as json_file:
        json.dump(matrices, json_file)

# Function to read the list of matrices from a JSON file
def read_matrices_from_json(file_name):
    with open(file_name, 'r') as json_file:
        matrices = json.load(json_file)
        return matrices
    

if __name__ == "__main__":
    n_list = [30,40,50,60,70,80,90,100,110,120]
    max_number = 500
    list_of_Bm = make_Bm_from_n_list(n_list, max_number)
    write_matrices_to_json('TestingSpeed/test_files/test_matrices_for_improved_LLL.json', list_of_Bm)

    n_list = np.arange(8,40 , 4)
    max_number = 500
    list_of_Bm = make_Bm_from_n_list(n_list, max_number)
    write_matrices_to_json('TestingSpeed/test_files/test_matrices_for_naive_LLL.json', list_of_Bm)