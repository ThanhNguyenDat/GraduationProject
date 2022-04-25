import json 
import os
import numpy as np
import open3d as o3d
from utils import *
from config import *

if False:
    with open("./results/json/plane_points.json") as f:
        data = json.load(f)
        n = 0
        for id, da in enumerate(data.keys()):
            # print(id)
            if id == n:
                print(da[id])
                pcd = create_pcd(data[da])
                o3d.visualization.draw_geometries([pcd])
                break
        # print(data.keys())
        # print(data["surface_1"])
        # print(type(data["surface_1"]))
        # print(len(data["surface_1"]))
        
        pcd = create_pcd(data["plane_seg_1"])
        print(pcd.points)
        # visualize
        # o3d.visualization.draw_geometries([pcd])

with open("./results/json/plane_model.json") as f, open("./results/json/plane_points.json") as f2:
    plane_model = json.load(f)
    base = plane_model["plane_model_0"]
    cam =  [1.373, -8.081, -4.511]
    
    theta = compute_theta(base, cam)
    # print(theta)
    # rotation
    R_z = Rz(theta)
    print(R_z)

    plane_points = json.load(f2)
    base_plane = plane_points["plane_seg_0"]
    # rotation
    base_plane = np.array(base_plane)
    base_plane = np.dot(R_z, base_plane.T).T
    print(base_plane)
    # visualize
    pcd = create_pcd(base_plane)
    o3d.visualization.draw_geometries([pcd])
    
    
    
    
    # translation
    # T_z = Tz(base, cam)

    # print(base)

    # print(type(data["plane_model_1"]))
    # print(len(data["plane_model_1"]))

