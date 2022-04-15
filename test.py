import json 
import os
import numpy as np
import open3d as o3d
from config import *

with open("./results/plane_points.json") as f:
    data = json.load(f)
    # print(data.keys())
    # print(data["surface_1"])
    # print(type(data["surface_1"]))
    # print(len(data["surface_1"]))
    
    pcd = o3d.geometry.PointCloud()
    # show xyz axis in the point cloud
    
    
    

    pcd.points = o3d.utility.Vector3dVector(np.asarray(data["plane_seg_0"]))
    pcd.paint_uniform_color([1, 0, 0])
    # pcd.points = o3d.utility.Vector3dVector(data["surface_1"])
    print(pcd.points)
    # visualize
    o3d.visualization.draw_geometries([pcd])
    # rotate
    R = pcd.get_rotation_matrix_from_xyz((0, 0, coor_z))
    pcd = pcd.rotate(R, center=(0,0,0))
    print(pcd.points)
    o3d.visualization.draw_geometries([pcd])

