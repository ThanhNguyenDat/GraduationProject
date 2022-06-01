import json 
import os
import numpy as np
import open3d as o3d
from config import *
from utils import *




pcd = o3d.io.read_point_cloud('./2.ply')
o3d.visualization.draw_geometries([pcd])

# #crop data
cropPCD = crop_point_cloud(pcd, range_x=[-0.1, 0.1], range_y=[0, 0.1], range_z=[-0.7, 0.1])
# o3d.visualization.draw_geometries([cropPCD])

downPCD = cropPCD.voxel_down_sample(voxel_size=0.01)
o3d.visualization.draw_geometries([downPCD])

# get base plane
plane_model, inliers = downPCD.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)
    
[a, b, c, d] = plane_model           
print(f"Plane equation:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")
vector_object = [a, b, c]
plane_pcd = pcd.select_by_index(inliers)
points_plane = np.asarray(plane_pcd.points)

# o3d.visualization.draw_geometries([plane_pcd])

# get base vector
vector_init_x = [1, 0, 0]
vector_init_y = [0, 1, 0]
vector_init_z = [0, 0, 1]
vector_object = [a, b, c]

# random vector robot
vector_robot = [0., 0.07, 0.35]

# rotaion z axis
# rotate matrix from vector
mat = rotation_matrix_3x3_from_vectors(vector_object, vector_init_z)

vec_transform = transform_matrix_from_vector(vector_object, vector_init_z)
pcd_rotation_z = downPCD.rotate(mat)
# pcd_rotation_z = downPCD.transform(vec_transform)

# visualize rotaion
o3d.visualization.draw_geometries([pcd_rotation_z])


# segmentation
plane_model, inliers = pcd_rotation_z.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)
    
[a, b, c, d] = plane_model           
print(f"Plane equation after rotation z axis:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")

vector_object = [a, b, c]

def convert_object_to_camera(vector_object, vector_robot):
    # convert to camera coordinate
    mat = np.eye(4)
    mat[:3, 3] = get_vector_init(vector_object, vector_robot)
    mat[:3,:3] = rotation_matrix_3x3_from_vectors(vector_object, vector_robot)
    return mat

mat = convert_object_to_camera(vector_object, vector_robot)
print("mat: ", mat)

# transform point cloud
pcd_transform = pcd_rotation_z.transform(mat)
o3d.visualization.draw_geometries([pcd_transform])

plane_model, inliers = pcd_transform.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)
    
[a, b, c, d] = plane_model           
print(f"Plane equation after rotation z axis:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")
vector_object = [a, b, c]

# rotation to robot coordinate
# mat = convert_object_to_camera(vector_object, vector_robot)
mat = rotation_matrix_3x3_from_vectors(vector_object, vector_robot)
# vec_trans = transform_matrix_from_vector(vector_object, vector_robot)
# pcd_rotation_z = pcd_transform.transform(vec_trans)
pcd_rotation_z = pcd_transform.rotate(mat)
o3d.visualization.draw_geometries([pcd_rotation_z])

plane_model, inliers = pcd_rotation_z.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)
    
[a, b, c, d] = plane_model           
print(f"Plane equation after rotation z axis:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")

vecotr_robot = 0 , 0, 0
vector_camera = 10, 10, 10
vecotr_obj = 10, 10, 0

