import numpy as np

def cal_theta_1(x, y, z):
    theta_1 = np.arctan2(y, z)
    return theta_1
    
def cal_theta_2(x, y, z, theta_1):
    theta_2 = np.arctan2(y, z) - theta_1
    return theta_2

def cal_theta_3(x, y, z, theta_1, theta_2):
    theta_3 = np.arctan2(y, z) - theta_1 - theta_2
    return theta_3

def cal_theta_4(x, y, z, theta_1, theta_2, theta_3):
    theta_4 = np.arctan2(y, z) - theta_1 - theta_2 - theta_3
    return theta_4

def cal_theta_5(x, y, z, theta_1, theta_2, theta_3, theta_4):
    theta_5 = np.arctan2(y, z) - theta_1 - theta_2 - theta_3 - theta_4
    return theta_5

