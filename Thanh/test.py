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
o3d.visualization.draw_geometries([cropPCD])

downPCD = cropPCD.voxel_down_sample(voxel_size=0.01)
o3d.visualization.draw_geometries([downPCD])

plane_seg(downPCD, visual_flag=True)

# # get base plane
# plane_model, inliers = downPCD.segment_plane(distance_threshold=0.01,
#                                                 ransac_n=3,
#                                                 num_iterations=1000)
    
# [a, b, c, d] = plane_model           
# print(f"Plane equation:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")
# vector_object = [a, b, c]
# plane_pcd = pcd.select_by_index(inliers)
# points_plane = np.asarray(plane_pcd.points)

# o3d.visualization.draw_geometries([plane_pcd])

# # get base vector
# vector_init_x = [1, 0, 0]
# vector_init_y = [0, 1, 0]
# vector_init_z = [0, 0, 1]
# vector_object = [a, b, c]

# # random vector robot
# vector_robot = [0., 0.07, 0.35]

# # rotaion z axis
# # rotate matrix from vector
# mat = rotation_matrix_3x3_from_vectors(vector_object, vector_init_z)

# vec_transform = transform_matrix_from_vector(vector_object, vector_init_z)

# pcd_rotation_z = downPCD.transform(vec_transform)

# # visualize rotaion
# o3d.visualization.draw_geometries([pcd_rotation_z])


# # segmentation
# plane_model, inliers = pcd_rotation_z.segment_plane(distance_threshold=0.01,
#                                                 ransac_n=3,
#                                                 num_iterations=1000)
    
# [a, b, c, d] = plane_model           
# print(f"Plane equation after rotation z axis:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")

# vector_object = [a, b, c]
# # convert to robot coordinate
# # translate matrix from vector object to vector robot
# mat_translate = translate_matrix_from_vector(vector_object, vector_robot)

# transform pcd
# pcd_translate = pcd_rotation_z.transform(mat_translate)

# o3d.visualization.draw_geometries([pcd_translate])

# # segmentation
# plane_model, inliers = pcd_translate.segment_plane(distance_threshold=0.01,
#                                                 ransac_n=3,
#                                                 num_iterations=1000)
    
# [a, b, c, d] = plane_model           
# print(f"Plane equation after translate robot:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")
# print("Matrix translate: ", mat_translate)

# vector_object = [a, b, c]
# vector_robot = [0., 0.07, 0.35]
# convert to robot coordinate

# # roation matrix from vector object to vector robot
# mat = rotation_matrix_3x3_from_vectors(vector_object, vector_robot)
# print("Matrix rotation: ", mat)

# vec_transform = transform_matrix_from_vector(vector_object, vector_robot)
# print("Matrix transform: ", vec_transform)

# pcd_rotation_robot = pcd_translate.transform(vec_transform)

# visualize rotaion
# o3d.visualization.draw_geometries([pcd_rotation_robot])

# segmentation
# plane_model, inliers = pcd_rotation_robot.segment_plane(distance_threshold=0.01,
#                                                 ransac_n=3,
#                                                 num_iterations=1000)
    
# [a, b, c, d] = plane_model           
# print(f"Plane equation rotaion robot:{a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")






# mat_strans = translate_matrix_from_vector(vector_object, vector_init_z)
# print(mat_strans.shape)
# # print(np.array(vector_object).shape)

# # vec_strans = mat_strans.dot(vector_object)

# # pcd
# print("pcd before rotation: ", np.asarray(pcd))
# print("pcd after rotation: ", np.asarray(pcd.transform(mat_strans)))

