import numpy as np
import math
import config
from config import *
CUBOID_EXTENT_METERS = 200

METERS_BELOW_START = 5
METERS_ABOVE_START = 30
def getCuboidPoints(start_position):
  return np.array([
    # Vertices Polygon1
    [start_position['x'] + (CUBOID_EXTENT_METERS / 2), start_position['y'] + (CUBOID_EXTENT_METERS / 2), start_position['z'] + METERS_ABOVE_START], # face-topright
    [start_position['x'] - (CUBOID_EXTENT_METERS / 2), start_position['y'] + (CUBOID_EXTENT_METERS / 2), start_position['z'] + METERS_ABOVE_START], # face-topleft
    [start_position['x'] - (CUBOID_EXTENT_METERS / 2), start_position['y'] - (CUBOID_EXTENT_METERS / 2), start_position['z'] + METERS_ABOVE_START], # rear-topleft
    [start_position['x'] + (CUBOID_EXTENT_METERS / 2), start_position['y'] - (CUBOID_EXTENT_METERS / 2), start_position['z'] + METERS_ABOVE_START], # rear-topright

    # Vertices Polygon 2
    [start_position['x'] + (CUBOID_EXTENT_METERS / 2), start_position['y'] + (CUBOID_EXTENT_METERS / 2), start_position['z'] - METERS_BELOW_START],
    [start_position['x'] - (CUBOID_EXTENT_METERS / 2), start_position['y'] + (CUBOID_EXTENT_METERS / 2), start_position['z'] - METERS_BELOW_START],
    [start_position['x'] - (CUBOID_EXTENT_METERS / 2), start_position['y'] - (CUBOID_EXTENT_METERS / 2), start_position['z'] - METERS_BELOW_START],
    [start_position['x'] + (CUBOID_EXTENT_METERS / 2), start_position['y'] - (CUBOID_EXTENT_METERS / 2), start_position['z'] - METERS_BELOW_START],
  ]).astype("float64") 
