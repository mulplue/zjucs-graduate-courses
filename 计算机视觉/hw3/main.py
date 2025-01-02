import os
import glob
import cv2
import numpy as np


class Calibrator():
    def __init__(self, board_size=(6,8), output_path="results") -> None:
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        h, w = board_size
        self.board_size = board_size
        self.objp = np.zeros((h*w,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:h,0:w].T.reshape(-1,2)

        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def calibrate(self, images_path, save=True):
        image_path_list = glob.glob(images_path)

        obj_points = []
        img_points = []
        for i, image_path in enumerate(image_path_list):
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            size = gray.shape[::-1]
            ret, corners = self.get_corner(gray)
            if ret:
                obj_points.append(self.objp)
                img_points.append(corners)
                cv2.drawChessboardCorners(img, self.board_size, corners, ret)
                if save:
                    save_path_i = os.path.join(self.output_path, 'corners_'+str(i)+'.jpg')
                    cv2.imwrite(save_path_i, img)
                    # print("Saving image: ", save_path_i)
        cv2.destroyAllWindows()

        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
        print("Camera matrix: ", self.mtx)
        print("Distortion coefficients: ", self.dist)
        print("Rotation vectors: ", self.rvecs)
        print("Translation vectors: ", self.tvecs)
    
    def undistort_image(self, image_path, save=True):
        img = cv2.imread(image_path)
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
        dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y+h,x:x+w]
        if save:
            save_path = os.path.join(self.output_path, 'undistorted_'+os.path.basename(image_path))
            cv2.imwrite(save_path, dst)
            # print("Saving image: ", save_path)
        return dst
    
    def get_bev(self, image_path, save=True):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = self.get_corner(gray)

        h, w = self.board_size
        objp = np.float32([[0,0], [h-1,0], [0,w-1], [h-1,w-1]]) * 150
        imgp = np.float32([corners[0], corners[h-1], corners[-h], corners[-1]])
        H = cv2.getPerspectiveTransform(imgp, objp)
        bev = cv2.warpPerspective(img, H, img.shape[:2][::-1])
        if save:
            save_path = os.path.join(self.output_path, 'bev_'+os.path.basename(image_path))
            cv2.imwrite(save_path, bev)
            # print("Saving image: ", save_path)
        return bev
    
    def get_corner(self, gray):
        ret, corners = cv2.findChessboardCorners(gray, self.board_size, None)
        if ret:
            corners_subpix = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), self.criteria)
            if [corners_subpix]:
                corners = corners_subpix
        return ret, corners
        

if __name__ == "__main__":
    calibrator = Calibrator((7,4))
    calibrator.calibrate("./data/*.jpg")
    calibrator.undistort_image("./data/2.jpg")
    calibrator.get_bev("./data/2.jpg")