import numpy as np
import math
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

# vector_init_x = (1, 0, 0)
# vector_init_y = (0, 1, 0)
# vector_init_z = (0, 0, 1)
# vector_object = (a, b, c)

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
        s = np.linalg.norm(v) # Equal euclidean distance
        
        # get theta angle
        # theta = np.arccos(c)
        # if s < 0:
        #    theta = -theta
        # get the axis
        # v = v / s
        # get the rotation matrix
        # mat = np.eye(3) + np.sin(theta) * np.vstack((v, -v)) + (1 - np.cos(theta)) * np.dot(v, v)
            
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    else:
        return np.eye(3)

def transform_matrix_from_vector(vec1, vec2=[0, 0, 1]):
    """ Find the transform matrix that aligns vec1 to vec2
    :param vec: A 3d "source" vector
    :return mat: A transform matrix (4x4) that maps vec1 to vec2
    """
    mat = np.eye(4)
    mat[:3,:3] = rotation_matrix_3x3_from_vectors(vec1, vec2)
    return mat
    

# mat = rotation_matrix_3x3_from_vectors(vector_object, vector_init_z)
# print(mat)
# # vec_rot = mat.dot(vector_object)

# vec_trans = transform_matrix_from_vector(vector_object, (0, 0, 1))
# print(vec_trans)

# # pcd after rotation
# print("pcd before rotation: ", np.asarray(pcd.points))
# print("pcd after rotation: ", np.asarray(pcd.transform(vec_trans)))

def get_vector_init(vector_object, vector_target):
    """
    Get the vector init.
    """
    return  np.array(vector_target) - np.array(vector_object)

def translate_matrix_from_vector(vector_object, vector_target):
    """
    Translate matrix from vector.
    """
    vector_init = get_vector_init(vector_object, vector_target)
    mat = np.eye(4)
    # mat[:3, 3] = np.array(vector_object) - np.array(vector_init)
    # mat = np.hstack((mat, np.array([0, 0, 0, 1])))
    mat[:3, 3] = vector_init#np.array(vector_object) - np.array(vector_init)
    return mat

# mat_strans = translate_matrix_from_vector(vector_object, vector_init_z)
# print(mat_strans.shape)
# # print(np.array(vector_object).shape)

# # vec_strans = mat_strans.dot(vector_object)

# # pcd
# print("pcd before rotation: ", np.asarray(pcd))
# print("pcd after rotation: ", np.asarray(pcd.transform(mat_strans)))

def convert_object_to_camera(vector_object, vector_robot):
    # convert to camera coordinate
    mat = np.eye(4)
    mat[:3, 3] = get_vector_init(vector_object, vector_robot)
    mat[:3,:3] = rotation_matrix_3x3_from_vectors(vector_object, vector_robot)
    return mat

def plane_seg(pcd, 
            threshold_points=100, 
            distance_threshold=0.01, 
            ransac_n=3, 
            num_iterations=1000, 
            visual_flag=False, 
            visual_n_th=0, 
            name_json_plane="plane_points.json",
            model_points="plane_model.json"):
    # Processing with loop
    i = 0
    list_plane = {}
    list_model = {}
    while  np.asarray(pcd.points).shape[0] > threshold_points:
        
        print("iteration: ", i)

        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                ransac_n=ransac_n,
                                                num_iterations=num_iterations)
    
        [a, b, c, d] = plane_model           
        print(f"Plane equation:{a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
            
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
        list_model["plane_model_"+str(i)] = [a, b, c]
        # print(list_plane)
        path_results = "./results/"
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

        if not os.path.isdir(path_save_json):
            os.mkdir(path_save_json)
            with open(path_save_json + model_points, "w") as f:
                json.dump(list_model, f)
        else:
            with open(path_save_json + model_points, "w") as f:
                json.dump(list_model, f)

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
