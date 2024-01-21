import numpy as np
from mylib import rotate_vector

green = np.array([0,1])
blue  = np.array([0,1])

for i in range (000,370,10):
    rot_vec= rotate_vector(blue,i)
    dot_product = np.dot(green, rot_vec)
    print(f'{i:03d}: {round(dot_product,3) :+0.3f}')

