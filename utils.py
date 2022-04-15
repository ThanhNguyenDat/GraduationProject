import numpy as np
from config import *
import open3d as o3d
import json
import os

# create point cloud from array or list of points
def create_pcd(data, color=None, path_save_ply=None) -> o3d.geometry.PointCloud():
    pcd = o3d.geometry.PointCloud()
    if type(data) == np.ndarray:
        pcd.points = o3d.utility.Vector3dVector(data)
    elif type(data) == list:
        pcd.points = o3d.utility.Vector3dVector(np.asarray(data))
    else:
        raise TypeError("data must be a numpy array or a list")
    if color is not None:
        pcd.colors = o3d.utility.Vector3dVector(color)
    if path_save_ply is not None:
        o3d.io.write_point_cloud(path_save_ply, pcd)
    return pcd


# crop the point cloud
def crop_point_cloud(pcd, range_x: list, range_y: list, range_z: list) -> o3d.geometry.PointCloud():
    assert len(range_x) == 2, "range_x must be a list of length 2 include min and max"
    assert len(range_y) == 2, "range_y must be a list of length 2 include min and max"
    assert len(range_z) == 2, "range_z must be a list of length 2 include min and max"

    n_xyz = np.asarray(pcd.points)
    mask_x = (n_xyz[:, 0] > range_x[0]) & (n_xyz[:, 0] < range_x[1])
    
    # print(mask_x)
    mask_y = (n_xyz[:, 1] > range_y[0]) & (n_xyz[:, 1] < range_y[1])
    mask_z = (n_xyz[:, 2] > range_z[0]) & (n_xyz[:, 2] < range_z[1])
    mask = mask_x & mask_y & mask_z
    # print(mask)
    cropPCD = create_pcd(n_xyz[mask])
    # cropPCD = o3d.geometry.PointCloud()
    # cropPCD.points = o3d.utility.Vector3dVector(n_xyz[mask])
    return cropPCD


# rotation point cloud
def rotation_point_cloud_from_xyz(pcd, xyz_rotation_angle: list) -> o3d.geometry.PointCloud():
    assert len(xyz_rotation_angle) == 3, "xyz_rotation_angle must be a list of length 3 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_xyz(xyz_rotation_angle, center=(0,0,0))
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_angle(pcd, angle: float) -> o3d.geometry.PointCloud():
    R = o3d.geometry.get_rotation_matrix_from_angle(angle, center=(0,0,0))
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_angle_axis(pcd, angle_axis: list) -> o3d.geometry.PointCloud():
    assert len(angle_axis) == 4, "angle_axis must be a list of length 4 include angle and axis"
    R = o3d.geometry.get_rotation_matrix_from_angle_axis(angle_axis[0], angle_axis[1:])
    pcd.rotate(R)
    return pcd
def rotation_point_cloud_from_quaternion(pcd, quaternion: list) -> o3d.geometry.PointCloud():
    assert len(quaternion) == 4, "quaternion must be a list of length 4 include x, y, z, w"
    R = o3d.geometry.get_rotation_matrix_from_quaternion(quaternion)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_euler_angles(pcd, euler_angles: list) -> o3d.geometry.PointCloud():
    assert len(euler_angles) == 3, "euler_angles must be a list of length 3 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_euler_angles(euler_angles)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_matrix(pcd, matrix: list) -> o3d.geometry.PointCloud():
    assert len(matrix) == 9, "matrix must be a list of length 9 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_matrix(matrix)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_quaternion_vector(pcd, quaternion_vector: list) -> o3d.geometry.PointCloud():
    assert len(quaternion_vector) == 4, "quaternion_vector must be a list of length 4 include x, y, z, w"
    R = o3d.geometry.get_rotation_matrix_from_quaternion_vector(quaternion_vector)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_rotation_vector(pcd, rotation_vector: list) -> o3d.geometry.PointCloud():
    assert len(rotation_vector) == 3, "rotation_vector must be a list of length 3 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_rotation_vector(rotation_vector)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_rotation_matrix(pcd, rotation_matrix: list) -> o3d.geometry.PointCloud():
    assert len(rotation_matrix) == 9, "rotation_matrix must be a list of length 9 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_rotation_matrix(rotation_matrix)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_translation_vector(pcd, translation_vector: list) -> o3d.geometry.PointCloud():
    assert len(translation_vector) == 3, "translation_vector must be a list of length 3 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_translation_vector(translation_vector)
    pcd.rotate(R)
    return pcd

def rotation_point_cloud_from_translation_matrix(pcd, translation_matrix: list) -> o3d.geometry.PointCloud():
    assert len(translation_matrix) == 9, "translation_matrix must be a list of length 9 include x, y, z"
    R = o3d.geometry.get_rotation_matrix_from_translation_matrix(translation_matrix)
    pcd.rotate(R)
    return pcd


def plane_seg(pcd, 
            threshold_points=100, 
            distance_threshold=0.01, 
            ransac_n=3, 
            num_iterations=1000, 
            visual_flag=False, 
            visual_n_th=0, 
            name_json_plane="plane_points.json"):
    # Processing with loop
    i = 0
    list_plane = {}

    while  np.asarray(pcd.points).shape[0] > threshold_points:
        if visual_flag:
            print("iteration: ", i)

        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                ransac_n=ransac_n,
                                                num_iterations=num_iterations)
        if visual_flag:
            [a, b, c, d] = plane_model           
            print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
            
        # Segment plane
        # Extract inliers and outliers
        plane_pcd = pcd.select_by_index(inliers)
        other_pcd = pcd.select_by_index(inliers, invert=True)
        
        # Count points in plane
        points_plane = np.asarray(plane_pcd.points)
        if visual_flag:
            print(f"Number of points in the plane: {points_plane.shape[0]}")
        
        # Count points in other
        points_others = np.asarray(other_pcd.points)
        if visual_flag:
            print(f"Number of points in the other: {points_others.shape[0]}")
        
        # Visualize
        if visual_flag:
            color_rand = np.random.rand(3)
            plane_pcd.paint_uniform_color(color_rand)
            o3d.visualization.draw_geometries([plane_pcd])
        # Break if no points left
        
        # create dict(list) to save plane points
        # plane = {ten_1: [points], ten_2: [points]}
        
        list_plane["plane_seg_"+str(i)] = points_plane.tolist()
        # print(list_plane)
        path_results = "./result/"
        if not os.path.isdir(path_results):
            os.mkdir(path_results)
            path_save_json = os.path.join(path_results, "json/")
        else:
            path_save_json = os.path.join(path_results, "json/")

        if not os.path.isdir(path_save_json):
            os.mkdir(path_save_json)
            with open(path_save_json + name_json_plane, "w") as f:
                json.dump(list_plane, f)
        else:
            with open(path_save_json + name_json_plane, "w") as f:
                json.dump(list_plane, f)

        # print("Point_others....................................: ", points_others.shape[0])
        if points_others.shape[0] < threshold_points:
            break
        
        # Update
        pcd = other_pcd

        # points_others.shape[0]
        # other = other.select_by_index(inliers, invert=True)
        i += 1
        if visual_flag:
            print("\n")
            print("===========================================================================================")
            print("\n")
    
    print("Total surfaces:", i)
    if visual_n_th != None:
        assert visual_n_th <= i, "visual_n_th: {} must be smaller than total surfaces: {}".format(visual_n_th, i)
        for id, da in enumerate(list_plane.keys()):
            if id == visual_n_th:
                print("Visualize with index pcd: ", id)
                pcd = create_pcd(list_plane[da])
                o3d.visualization.draw_geometries([pcd])
                break
    return list_plane 
