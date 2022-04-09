import json 
import os
import numpy as np
import open3d as o3d

with open("./results/plane_points.json") as f:
    data = json.load(f)
    # print(data.keys())
    # print(data["surface_1"])
    # print(type(data["surface_1"]))
    # print(len(data["surface_1"]))
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.asarray(data["surface_1"]))
    # pcd.points = o3d.utility.Vector3dVector(data["surface_1"])
    print(pcd.points)
    # visualize
    o3d.visualization.draw_geometries([pcd])
