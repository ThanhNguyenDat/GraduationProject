import numpy as np
import time


a2 = 100
a3 = 100
a5 = 100
d1 = 100
d4 = 100
    
def theta2sc(theta):
    return np.sin(theta), np.cos(theta)

def sc2theta(s, c):
    return np.arctan2(s, c)

def get_pos_p(theta_1, theta_2, theta_3, theta_4, theta_5):

    min = time.localtime().tm_min
    sec = time.localtime().tm_sec
    s1, c1 = theta2sc(theta_1)
    s2, c2 = theta2sc(theta_2)
    # s3, c3 = theta2sc(theta_3)
    s4, c4 = theta2sc(theta_4)
    s5, c5 = theta2sc(theta_5)
    c23, s23 = theta2sc(theta_2 + theta_3)
    px = -d4 * c1 * c23 - a3 * c1 * s23 - a5 * c5 * s1 * s4 - a2 * s2 * c1 - a5 * c1 * s5 * c23 - a5 * c1 * c4 * c5 * s23
    py = -d4 * s1 * c23 - a3 * s1 * s23 - a5 * c5 * c1 * s4 - a2 * s2 * s1 - a5 * s1 * s5 * s23 - a5 * s1 * c4 * c5 * s23
    pz = d1 + a3 * c23 + a2 * c2 - d4 * s23 - a5 * s5 * s23 + a5 * c4 * c5 * c23
    phi = theta_2 + theta_3 + theta_4
    gramma = theta_1 + theta_5

    return px, py, pz, phi, gramma

def cal_m(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5):
    s4, c4 = theta2sc(theta_4)
    s5, c5 = theta2sc(theta_5)
    c23, s23 = theta2sc(theta_2 + theta_3)
    # m = a3*s23 + a2*s2
    m = np.sqrt(x**2 + y**2) - d4*c23 - a5*s5*c23 - a5*c4*c5*s23 - a5*c5*s4
    return m

def cal_n(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5):
    s4, c4 = theta2sc(theta_4)
    s5, c5 = theta2sc(theta_5)
    c23, s23 = theta2sc(theta_2 + theta_3)
    # n = a3*c23 + a2*c2
    n = z - d1 + d4*s23 + a5*s5*s23 - a5*c4*c5*c23
    return n

def cal_theta_1(y, z):
    theta_1 = np.arctan2(y, z)
    return theta_1

def cal_theta_5(gramma, theta_1):
    theta_5 = gramma - theta_1
    return theta_5
    
    
# def cal_theta_3(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5):
#     s23, c23 = theta2sc(theta_2 + theta_3)
#     s2, c2 = theta2sc(theta_2)
#     s4, c4 = theta2sc(theta_4)
#     s5, c5 = theta2sc(theta_5)
#     m = cal_m(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5)
#     # m = a3*s23 + a2*s2
#     n = cal_n(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5)
#     # n = a3*c23 + a2*c2
#     pass

# def cal_theta_2(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5):
#     s3, c3 = theta2sc(theta_3)
#     m = cal_m(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5)
#     # m = a3*s23 + a2*s2
#     n = cal_n(x, y, z, theta_1, theta_2, theta_3, theta_4, theta_5)
#     # n = a3*c23 + a2*c2
#     D = (a3*c3 + a2) ** 2 + (a3*s3) ** 2
#     s2 = None


# def cal_theta_4(gramma, theta_2, theta_3):
#     return gramma - theta_2 - theta_3



def cal_theta_2(x, y, z, theta_1):
    theta_2 = np.arctan2(y, z) - theta_1
    return theta_2

def cal_theta_3(x, y, z, theta_1, theta_2):
    theta_3 = np.arctan2(y, z) - theta_1 - theta_2
    return theta_3

def cal_theta_4(x, y, z, theta_1, theta_2, theta_3):
    theta_4 = np.arctan2(y, z) - theta_1 - theta_2 - theta_3
    return theta_4
