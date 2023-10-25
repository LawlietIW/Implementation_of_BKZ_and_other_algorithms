import numpy as np

# Define the row matrix as a 2D NumPy array
row_matrix = np.array([[1, 2, 3], [2, 4, -1]])  # Example rows of the matrix

# Define the vector as a 1D NumPy array
vector = np.array([5,2,5])  # Example vector to be projected

# Calculate the projection of the vector onto the subspace spanned by the rows of the matrix
projection = vector - np.dot(vector, row_matrix.T) @ np.linalg.inv(row_matrix @ row_matrix.T) @ row_matrix

# Print the projection result
print("Projection of the vector onto the subspace spanned by the rows of the matrix:")
print(projection)
