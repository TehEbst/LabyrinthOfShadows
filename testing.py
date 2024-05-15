import random

import numpy as np

matrix = np.zeros((2, 2, 2))
tup = 1, 1
print(matrix[(*tup, 0)])