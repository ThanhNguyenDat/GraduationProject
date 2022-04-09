import json 
import os
import numpy as np
import open3d as o3d
from utils import *
with open("./results/plane_points.json") as f:
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
