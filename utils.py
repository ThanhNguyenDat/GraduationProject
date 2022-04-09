import numpy as np
import math
import config
from config import *
import open3d as o3d
import json


def crop(pcd, range_x, range_y, range_z):
  n_xyz = np.asarray(pcd.points)
  mask_x = (n_xyz[:, 0] > range_x[0]) & (n_xyz[:, 0] < range_x[1])
  
  # print(mask_x)
  mask_y = (n_xyz[:, 1] > range_y[0]) & (n_xyz[:, 1] < range_y[1])
  mask_z = (n_xyz[:, 2] > range_z[0]) & (n_xyz[:, 2] < range_z[1])
  mask = mask_x & mask_y & mask_z
  # print(mask)
  cropPCD = o3d.geometry.PointCloud()
  cropPCD.points = o3d.utility.Vector3dVector(n_xyz[mask])
  return cropPCD


def plane(pcd, threshold_points=100, distance_threshold=0.01, ransac_n=3, num_iterations=1000):
    # Processing with loop
    i = 1
    dict_plane = {}

    while  pcd.shape[0] > threshold_points:
        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                ransac_n=ransac_n,
                                                num_iterations=num_iterations)
        [a, b, c, d] = plane_model           
        print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
        
        print("Processing with the {} loop".format(i))
        # Segment plane

        # Extract inliers and outliers
        plane = pcd.select_by_index(inliers)
        other = pcd.select_by_index(inliers, invert=True)
        
        # Count points in plane
        points_plane = np.asarray(plane.points)
        print(f"Number of points in the plane: {points_plane.shape[0]}")
        
        # Count points in other
        points_others = np.asarray(other.points)
        print(f"Number of points in the other: {points_others.shape[0]}")
        # Visualize
        # if visual_flag:
        color_rand = np.random.rand(3)

        plane.paint_uniform_color(color_rand)

        o3d.visualization.draw_geometries([plane])
        # Break if no points left
        
        # create dict(list) to save plane points
        # plane = {ten_1: [points], ten_2: [points]}
        
        dict_plane["surface_"+str(i)] = points_others.tolist()
        with open("./plane.json", "w") as f:
            json.dump(dict_plane, f)

        
        print("Point_others....................................: ", points_others.shape[0])
        if points_others.shape[0] < threshold_points:
            break
        
        # Update
        pcd = other

        # points_others.shape[0]
        # other = other.select_by_index(inliers, invert=True)
        i += 1
        print("Total surfaces:", i)
        
        # return plane