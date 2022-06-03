# from utils import *
import numpy as np

def get_vector_init(vector_object, vector_target):
    """
    Get the vector init.
    """
    return np.array(vector_object) - np.array(vector_target)

coor_O = np.array([0, 0, 0]) # coordinate base on O
coor_c_for_O = np.array([10, 10, 3]) # coordinate camera for base 0,0,0
coor_p_for_C = np.array([0, 0, 3]) # coordinate P points for camera
coor_p_for_C_2 = np.array([5, 6, 4])

def get_coor_p_for_O(coor_0, coor_c_for_O, coor_p_for_C):
    """
    Get the coordinate P points for base 0,0,0.
    """
    return coor_p_for_C - coor_c_for_O - coor_0

coor_P = get_coor_p_for_O(coor_O, coor_c_for_O, coor_p_for_C)    
print(coor_P)

