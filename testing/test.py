import numpy as np

matrix = np.array(([11, 12, 13], [21, 22, 23], [31, 32, 33], [11, 12, 13], [21, 22, 23], [31, 32, 33]))
split = int((len(matrix))/2)
print(matrix[0:split])