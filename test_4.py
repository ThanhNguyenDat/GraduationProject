# from utils import *
import numpy as np

def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, np.cos(theta),-np.sin(theta)],
                   [ 0, np.sin(theta), np.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                   [ np.sin(theta), np.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])


def get_vector_init(vector_object, vector_target):
    """
    Get the vector init.
    """
    return np.array(vector_object) - np.array(vector_target)

coor_O = np.array([0, 0, 0]) # coordinate base on O
coor_c_for_O = np.array([10, 10, 3]) # coordinate camera for base 0,0,0
coor_p_for_C = np.array([0, 0, 3]) # coordinate P points for camera
coor_p_for_C_2 = np.array([5, 6, 4]) # coordinate P_2 points for camera


def get_coor_p_for_O(coor_0, coor_c_for_O, coor_p_for_C):
    """
    Get the coordinate P points for base 0,0,0.
    """
    coor_p_for_C[2] = -coor_p_for_C[2]
    return coor_0 + coor_c_for_O + coor_p_for_C

coor_P = get_coor_p_for_O(coor_O, coor_c_for_O, coor_p_for_C)    
print("Toa do diem P so voi diem O", coor_P)
# [10, 10, 0]


coor_P_2 = get_coor_p_for_O(coor_O, coor_c_for_O, coor_p_for_C_2)
print("Toa do diem P2 so voi diem O", coor_P_2)
# [15, 16, -1]