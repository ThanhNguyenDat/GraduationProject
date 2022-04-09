import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import subprocess
import sys
import os
import glob
import json
import argparse
# try:
#   import open3d as o3d
# except:
#   subprocess.check_call([sys.executable, "-m", "pip", "install", "open3d"])
#   import open3d as o3d
import open3d as o3d
from config import *
from utils import *

def main(opt):
    z, y, z = 1.373, -8.081, -4.511
    N = 9.356
    
    # read ply file
    # path = img_dir + "/1.ply"
    # path = "./images/158.ply"
    path = opt.path_img
    pcd = o3d.io.read_point_cloud(path)
    # ply_file.paint_uniform_color([1, 0.706, 0])
    
    #crop data
    cropPCD = crop(pcd, [-0.75, 0.25], [-1, 1], [-1.25, -0.75])
    o3d.visualization.draw_geometries([cropPCD])
    
    # down sampling
    downPCD = cropPCD.voxel_down_sample(voxel_size = 0.01)
    if opt.visual:
        o3d.visualization.draw_geometries([downPCD])
    
    # plane segmentation
    plane = plane(downPCD, threshold_points=opt.threshold_points, distance_threshold=opt.distance_threshold, ransac_n=opt.ransac_n, num_iterations=opt.num_iterations, visual_flag=opt.visual)

def parse_args(known_args=None):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path_img', type=str, default='./images/158.ply')
    parser.add_argument('--visual', type=bool, default=False)
    parser.add_argument('--threshold_points', type=int, default=100)
    parser.add_argument('--distance_threshold', type=float, default=0.01)
    parser.add_argument('--ransac_n', type=int, default=3)
    parser.add_argument('--num_iterations', type=int, default=1000)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    opt = parse_args()
    main(opt)