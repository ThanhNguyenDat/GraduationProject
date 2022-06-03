from inspect import CORO_RUNNING
import open3d as o3d
import numpy as np
from utils import *

coor_robot = np.array([0.01, 0.01, 0.01])
coor_camera = np.array([0.60, 0.60, 0.60])
coor_obj = np.array([0.80, 0.10, 0.6])

# show coordinate box
robot_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.9, origin=coor_robot, )
camera_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=coor_camera, )
object_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3, origin=coor_obj, )

print("Center of robot: ", robot_coordinate.get_center())
print("Center of camera: ", camera_coordinate.get_center())
print("Center of object: ", object_coordinate.get_center())

# Rotaion camera
R = camera_coordinate.get_rotation_matrix_from_xyz((np.pi/2, 0, 0))
camera_coordinate.rotate(R, center=camera_coordinate.get_center())
print("Center of camera: ", camera_coordinate.get_center())


# show he toa do
box = o3d.geometry.TriangleMesh.create_box(width=0.1, height=0.2, depth=0.3,create_uv_map=True)

# show pcd
# o3d.visualization.draw_geometries([box, robot_coordinate, camera_coordinate,])
# show coordinate box


# print("coor_box: ", coor_box)
# translate the box to the coor_box
_mat = translate_matrix_from_vector([0, 0, 0], coor_obj)
box = box.transform(_mat)

# rotaion the box to the random angle
_mat = rotation_matrix_3x3_from_vectors(coor_robot, [np.pi/4, 1, np.pi/2])
# _mat =  transform_matrix_from_vector([0.01, 0.01, 0.01], [np.pi/4, 1, np.pi/2])
box.rotate(_mat, center=box.get_center())
# box.transform(_mat)

# rotaion coordinate box to the random angle
object_coordinate.rotate(_mat, center=box.get_center())
# object_coordinate.transform(_mat)

# init box
o3d.visualization.draw_geometries([box, robot_coordinate, camera_coordinate, object_coordinate])
######### DONE INIT


def compute_theta_between_vectors(v1, v2):
    """
    compute the angle between two vectors
    return the angle in radian with 3 dimension (x, y, z)
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    print(v1.shape, v2.shape)
    return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    # cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    # theta = np.arccos(cos_theta)
    # return theta

# compute theta betwween robot and camera
theta_robot_camera = compute_theta_between_vectors([np.pi, 0, np.pi/2], coor_camera)
print("theta_robot_camera: ", theta_robot_camera)



# PROCESS HERE
# 1. translate the box to the robot coordinate
print(coor_obj, coor_robot)
print(get_vector_init(coor_obj, coor_robot))
_mat = translate_matrix_from_vector(coor_obj, coor_robot)

print("_mat: ", _mat)
box = box.transform(_mat)
# translate the coordinate box to the robot coordinate
object_coordinate.transform(_mat)

o3d.visualization.draw_geometries([box, robot_coordinate, camera_coordinate, object_coordinate])


# segmation is only applied for the plane pcd (.ply)
# [np.pi/4, 1, np.pi/2] get segmantation
# 2. rotate the box to the camera coordinate
_mat = rotation_matrix_3x3_from_vectors([np.pi/4, 1, np.pi/2], coor_robot)
box.rotate(_mat, center=box.get_center())
object_coordinate.rotate(_mat, center=box.get_center())

o3d.visualization.draw_geometries([box, robot_coordinate, camera_coordinate, object_coordinate])
