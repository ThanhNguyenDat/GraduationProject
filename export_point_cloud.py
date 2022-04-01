## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import time
from config import *

# Create Trackbar for Threshold
# cv2.namedWindow('Depth Image')
cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('FPS', 'RealSense', 0, 50, lambda x: x+1)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

fps = cv2.getTrackbarPos('FPS', 'RealSense')
print(fps)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, fps)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, fps)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, fps)

# Start streaming
pipeline.start(config)

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
colorizer = rs.colorizer()

try:
    while True:
        # print(pipeline)
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        time.sleep(2)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        colorized = colorizer.process(frames)
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))
        
        # Flip camera image
        images = cv2.flip(images, 1)
        
        # Create save_to_ply object
        ply = rs.save_to_ply("1.ply")
        
        # Set options to the desired values
        # In this example we'll generate a textual PLY with normals (mesh is already created by default)
        ply.set_option(rs.save_to_ply.option_ply_binary, False)
        ply.set_option(rs.save_to_ply.option_ply_normals, False)

        print("Saving to 1.ply...")
        # Apply the processing block to the frameset which contains the depth frame and the texture
        ply.process(colorized)
        print("Done")

        # Save images
        import os
        # Create directory if not exist
        if not os.path.exists('images'):
            os.mkdir('images')
        
        if count // 2 == 0:
            if len(os.listdir("./images"))!=10:
                cv2.imwrite("./images/image_" + str(count) + ".png", images)    
        count += 1

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        
finally:

    # Stop streaming
    pipeline.stop()