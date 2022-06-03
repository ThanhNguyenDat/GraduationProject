import numpy as np

count = 0
a_x, a_y, a_z = 1.373, -8.081, -4.511
coor_x = np.arccos(a_x / 9.81)
coor_y = np.arccos(a_y / 9.81)
coor_z = np.arccos(a_z / 9.81)
print(coor_x, coor_y, coor_z)
N = 9.356
CUBOID_EXTENT_METERS = 200

METERS_BELOW_START = 5
METERS_ABOVE_START = 30

img_dir = "./images/"
