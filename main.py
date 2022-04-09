import argparse
import math
import os
import random
import sys
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import open3d as o3d
from config import *
from utils import *


def main(opt):
    # read ply file
    # path = img_dir + "/1.ply"
    # path = "./images/158.ply"
    path = opt.path_img
    pcd = o3d.io.read_point_cloud(path)
    # ply_file.paint_uniform_color([1, 0.706, 0])
    
    #crop data
    cropPCD = crop(pcd, [-0.75, 0.25], [-1, 1], [-1.25, -0.75])
    if opt.visual:
        o3d.visualization.draw_geometries([cropPCD])
    
    # check rotation z axis
    # pcd_rotate = pcd.rotate(axis=[0, 0, 1], angle=math.pi/2)
    # o3d.visualization.draw_geometries([pcd_rotate])


    # down sampling
    downPCD = cropPCD.voxel_down_sample(voxel_size=0.01)
    if opt.visual:
        o3d.visualization.draw_geometries([downPCD])
    
    # plane segmentation
    _plane_seg = plane_seg(downPCD, threshold_points=opt.threshold_points, distance_threshold=opt.distance_threshold, ransac_n=opt.ransac_n, num_iterations=opt.num_iterations, visual_flag=opt.visual, path_save_json=opt.path_save_json)

def parse_args(known=False):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path_img', type=str, default='./images/158.ply', help="path to the ply file")
    parser.add_argument('--visual', type=bool, default=False, help="visualize the result")
    parser.add_argument('--visual_n_th', type=int, default=1, help="visualize the n'th result")
    parser.add_argument('--threshold_points', type=int, default=100, help="threshold points")
    parser.add_argument('--distance_threshold', type=float, default=0.01, help="distance threshold")
    parser.add_argument('--ransac_n', type=int, default=3, help="ransac n")
    parser.add_argument('--num_iterations', type=int, default=1000, help="num iterations")
    parser.add_argument('--path_save_json', type=str, default='./results/', help="path to save the json file")
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_args()
    main(opt)