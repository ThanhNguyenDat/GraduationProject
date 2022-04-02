import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import subprocess
import sys
import os
import glob
import json
# try:
#   import open3d as o3d
# except:
#   subprocess.check_call([sys.executable, "-m", "pip", "install", "open3d"])
#   import open3d as o3d
import open3d as o3d
from config import *
from utils import *

z, y, z = 1.373, -8.081, -4.511
N = 9.356

# read ply file
# path = img_dir + "/1.ply"
path = "./images/158.ply"
pcd = o3d.io.read_point_cloud(path)
# ply_file.paint_uniform_color([1, 0.706, 0])
#crop data

cropPCD = crop(pcd, [-0.75, 0.25], [-1, 1], [-1.25, -0.75])
o3d.visualization.draw_geometries([cropPCD])

downPCD = cropPCD.voxel_down_sample(voxel_size = 0.01)
o3d.visualization.draw_geometries([downPCD])

plane = plane(downPCD)
