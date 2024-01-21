import numpy as np
from math import cos, sin
    
def rotate_vector(vec,deg):
    theta = np.deg2rad(deg)
    rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    return np.dot(vec,rot)    

