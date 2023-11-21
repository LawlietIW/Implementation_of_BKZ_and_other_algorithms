import numpy as np
import json
import pprint

# Assuming you have a list of 2D arrays
list_of_arrays = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]

# Convert NumPy arrays to lists for JSON serialization
# list_of_arrays_as_rows = [[arr_row.tolist() for arr_row in arr] for arr in list_of_arrays]

# Save arrays to a JSON file with separators between arrays
with open('arrays_file.json', 'w') as json_file:
    
    json.dump(list_of_arrays_as_rows, json_file, indent=4)
