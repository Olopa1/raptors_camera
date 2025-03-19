'''
Sample Usage:-
python calibration.py --dir calibration_checkerboard/ --square_size 0.024
'''

import numpy as np
import cv2
import os
import argparse

def calibrate(dirpath, square_size, width, height, visualize=False):
    """Apply camera calibration operation for images in the given directory path."""

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points
    objp = np.zeros((height * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)
    objp *= square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3D point in real-world space
    imgpoints = []  # 2D points in the image plane.

    # Read only valid image files
    valid_extensions = ('.png', '.jpg', '.jpeg')
    images = [f for f in os.listdir(dirpath) if f.lower().endswith(valid_extensions)]

    for i, fname in enumerate(images):
        print(f"Processing image {i + 1}/{len(images)}: {fname}")
        img_path = os.path.join(dirpath, fname)

        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read {fname}. Skipping.")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Optionally visualize
            if visualize:
                img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
                
                cv2.imshow('img', cv2.resize(img, (1280,720)))
                cv2.waitKey(0)
        else:
            print(f"Warning: Chessboard not found in {fname}. Skipping.")

    cv2.destroyAllWindows()

    # Perform calibration
    if len(objpoints) == 0 or len(imgpoints) == 0:
        print("Error: Not enough valid images to perform calibration.")
        return None

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return ret, mtx, dist, rvecs, tvecs

if __name__ == '__main__':

    
    dirpath = '/home/raptors/Desktop/wojtek/Calibration/USB3'
    # 2.4 cm == 0.024 m
    square_size = 0.025 #zmierzyc
    width = 10
    height = 7

    ret, mtx, dist, rvecs, tvecs = calibrate(dirpath, square_size, visualize=True, width=width, height=height)
    
    img = cv2.imread(dirpath+'/USB1_50.png')
    if img is None :
        print('Failed to open the image!')
        exit(1)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
 
# crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('calibresult2.png', dst)
    
    print("##################### mtx:")
    print(mtx)
    print("##################### dist:")
    print(dist)

    np.save("calibration_matrix", mtx)
    np.save("distortion_coefficients", dist)
