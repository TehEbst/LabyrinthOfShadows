import numpy as np

x = 1, 0
z = 1

yuh = np.zeros((2, 2, 2))
yuh[:, :, 0] = 6

print(yuh)
print()
print(yuh[:, 0, 0])

print(np.any(yuh[:, :, 0] != 6))
