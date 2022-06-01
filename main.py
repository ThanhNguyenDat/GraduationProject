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
    
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=[-2, -2, -2])

    # read ply file
    pcd = o3d.io.read_point_cloud(opt.path_img)
    
    #crop data
    cropPCD = crop_point_cloud(pcd, range_x=[-0.75, 0.25], range_y=[-1, 1], range_z=[-1.25, -0.75])
    
    # rotate the point cloud
    # rotatePCD = rotation_point_cloud_from_xyz(cropPCD, xyz_rotation_angle=(0, 0, coor_z))
    # compute the theta of the z axis
    print("cropPCD.points: ", np.asarray(cropPCD.points))
    
    
    # Compute theta
    # theta = compute_theta(cropPCD.points[0], cropPCD.points[-1])
    # print("theta: ", theta)

    # Rotation Rz
    
    print("PCD: ", cropPCD.points)
    # if opt.visual:
    #     o3d.visualization.draw_geometries([rotatePCD])
    

    # down sampling
    downPCD = cropPCD.voxel_down_sample(voxel_size=0.01)
    if opt.visual:
        o3d.visualization.draw_geometries([downPCD])
    
    # plane segmentation
    _plane_seg = plane_seg(downPCD, 
                        threshold_points=opt.threshold_points, 
                        distance_threshold=opt.distance_threshold, 
                        ransac_n=opt.ransac_n, 
                        num_iterations=opt.num_iterations, 
                        visual_flag=opt.visual, 
                        visual_n_th=opt.visual_n_th, 
                        name_json_plane=opt.name_json_plane)

def parse_args(known=False):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path_img', type=str, default='./images/158.ply', help="path to the ply file")
    parser.add_argument('--visual', type=bool, default=False, help="visualize the result")
    parser.add_argument('--visual_n_th', type=int, default=None, help="visualize the n'th result")
    parser.add_argument('--threshold_points', type=int, default=100, help="threshold points")
    parser.add_argument('--distance_threshold', type=float, default=0.01, help="distance threshold")
    parser.add_argument('--ransac_n', type=int, default=3, help="ransac n")
    parser.add_argument('--num_iterations', type=int, default=1000, help="num iterations")
    parser.add_argument('--name_json_plane', type=str, default='plane_points.json', help="path to save the plane json file")
    parser.add_argument('--name_json_model', type=str, default='plane_model.json', help="path to save the model json file")
    parser.add_argument('--coor_z', type=float, default=0.5, help="coor z")


    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_args(known=True)
    main(opt)