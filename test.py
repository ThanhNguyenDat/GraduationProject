import json 
import os
import numpy as np
import open3d as o3d
from config import *
from utils import *

pcd = o3d.io.read_point_cloud('./1.ply')
# o3d.visualization.draw_geometries([pcd])

# #crop data
cropPCD = crop_point_cloud(pcd, range_x=[-0.5, 0.5], range_y=[-0.5, 0.5], range_z=[-0.3, 0])


downPCD = cropPCD.voxel_down_sample(voxel_size=0.01)
# o3d.visualization.draw_geometries([downPCD])

plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)
    
[a, b, c, d] = plane_model           
print(f"Plane equation:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")

plane_pcd = pcd.select_by_index(inliers)
points_plane = np.asarray(plane_pcd.points)

# plane_pcd.paint_uniform_color()
# o3d.visualization.draw_geometries([plane_pcd])

vector_init_x = (1, 0, 0)
vector_init_y = (0, 1, 0)
vector_init_z = (0, 0, 1)
vector_object = (a, b, c)
    
def rotation_matrix_3x3_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) that maps vec1 to vec2
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    if any(v): #if not all zeros then 
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    else:
        return np.eye(3)

def transform_matrix_from_vector(vec, axis=(0, 0, 1)):
    """ Find the transform matrix that aligns vec1 to vec2
    :param vec: A 3d "source" vector
    :return mat: A transform matrix (4x4) that maps vec1 to vec2
    """
    mat = np.eye(4)
    mat[:3,:3] = rotation_matrix_3x3_from_vectors(vec, axis)
    return mat
    

mat = rotation_matrix_3x3_from_vectors(vector_object, vector_init_z)
print(mat)
# vec_rot = mat.dot(vector_object)

vec_trans = transform_matrix_from_vector(vector_object)
print(vec_trans)

# pcd after rotation
print("pcd before rotation: ", np.asarray(pcd.points))
print("pcd after rotation: ", np.asarray(pcd.transform(vec_trans)))

o3d.visualization.draw_geometries([plane_pcd])
pcd_rotation = plane_pcd.transform(vec_trans)
# plane segmentaion

plane_model, inliers = pcd_rotation.segment_plane(distance_threshold=0.01,
                                                ransac_n=3,
                                                num_iterations=1000)

[a, b, c, d] = plane_model           
print(f"Plane equation:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")
# output Plane equation:0.00008x + -0.00003y + 1.00000z + 0.23855 = 0

