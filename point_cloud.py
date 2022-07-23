import numpy as np
import open3d as o3d

class PointCloud():
    def __init__(self, data):
        self.data = data
        self.pcd = o3d.geometry.PointCloud(data)
    
    def _check_pcd(self):
        if isinstance(self.data, str):
            self.pcd = o3d.io.read_point_cloud(self.data)
        elif isinstance(self.data, o3d.geometry.PointCloud):
            self.pcd.points = self.data.points
        if isinstance(self.data, np.ndarray):
            self.pcd.points = o3d.utility.Vector3dVector(self.data)
        elif isinstance(self.data, list):            
            self.pcd.points = o3d.utility.Vector3dVector(np.asarray(self.data))
        elif not isinstance(self.pcd, o3d.geometry.PointCloud):
            raise ValueError("pcd must be a o3d.geometry.PointCloud")
        # return self.pcd
    
    def _create_pcd(self, color=None, path_save_ply:str=None) -> o3d.geometry.PointCloud():
        # self.pcd = o3d.geometry.PointCloud()
        self._check_pcd()
        
        if not isinstance(color, type(None)):
            self.pcd.colors = o3d.utility.Vector3dVector(color)
        
        if path_save_ply:
            o3d.io.write_point_cloud(path_save_ply, self.pcd)
        return self.pcd

    def crop_point_cloud(self, range_x: list, range_y: list, range_z: list) -> o3d.geometry.PointCloud():
        assert len(range_x) == 2, "range_x must be a list of length 2 include min and max"
        assert len(range_y) == 2, "range_y must be a list of length 2 include min and max"
        assert len(range_z) == 2, "range_z must be a list of length 2 include min and max"
        
        self._check_pcd()
        n_xyz = np.asarray(self.pcd.points)
        mask_x = (n_xyz[:, 0] > range_x[0]) & (n_xyz[:, 0] < range_x[1])
        
        # print(mask_x)
        mask_y = (n_xyz[:, 1] > range_y[0]) & (n_xyz[:, 1] < range_y[1])
        mask_z = (n_xyz[:, 2] > range_z[0]) & (n_xyz[:, 2] < range_z[1])
        mask = mask_x & mask_y & mask_z
        # print(mask)
        cropPCD = self._create_pcd(n_xyz[mask])
        # cropPCD = o3d.geometry.PointCloud()
        # cropPCD.points = o3d.utility.Vector3dVector(n_xyz[mask])
        return cropPCD
    
    # Matrix rotation 
    def Rx(theta:float):
        return np.matrix([[ 1, 0           , 0           ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])
    
    
    def Ry(theta:float):
        return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                        [ 0           , 1, 0           ],
                        [-np.sin(theta), 0, np.cos(theta)]])
    
    def Rz(theta:float):
        return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                        [ np.sin(theta), np.cos(theta) , 0 ],
                        [ 0           , 0            , 1 ]])
        
    # Transformation matrix
    def rotate_point_cloud(self, theta:float, axis:str) -> o3d.geometry.PointCloud():
        if axis == "x":
            R = self.Rx(theta)
        elif axis == "y":
            R = self.Ry(theta)
        elif axis == "z":
            R = self.Rz(theta)
        else:
            raise ValueError("axis must be x, y or z")
        n_xyz = np.asarray(self.pcd.points)
        n_xyz = np.matmul(R, n_xyz.T).T
        return self._create_pcd(n_xyz)
    
    # Translation matrix
    def translate_point_cloud(self, x:float, y:float, z:float) -> o3d.geometry.PointCloud():
        T = np.matrix([[1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z]])
        n_xyz = np.asarray(self.pcd.points)
        n_xyz = np.matmul(T, n_xyz.T).T
        return self._create_pcd(n_xyz)
    
if __name__=="__main__":
    pcd = o3d.io.read_point_cloud('./2.ply')

    pointCloud = PointCloud(pcd)

    o3d.visualization.draw_geometries([pcd])
    cropPCD = pointCloud.crop_point_cloud(range_x=[-0.1, 0.1], range_y=[0, 0.1], range_z=[-0.7, 0.1])
    o3d.visualization.draw_geometries([cropPCD])