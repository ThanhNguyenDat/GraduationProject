import json
import numpy as np
import open3d as o3d 

a = json.load(open("./plane.json"))
print(a.keys())

surface_1 = a["surface_1"]
print(surface_1)
# o3d.visualization.draw_geometries([surface_1])
o3d.visualization.draw_geometries([surface_1])