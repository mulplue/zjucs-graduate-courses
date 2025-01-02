# HW3: 

## 作业要求

![requirement](/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/imgs/requirement.png)


## 运行

### 环境

```bash
python==3.9.18
opencv-python==4.10.0.84
numpy==1.26.4
```

### 运行

```bash
cd hw3
python main.py
```



## 实现

### 数据来源

- iphone 15前置摄像头，拍摄电脑展示图片

### 相机标定

- 主要流程如下

  ```python
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
          print("Saving image: ", save_path_i)
  ```

- 得到相机参数

  ```python
  Camera matrix:  [[1.27338517e+03 0.00000000e+00 8.60161638e+02]
   [0.00000000e+00 1.27334847e+03 6.39698502e+02]
   [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
  Distortion coefficients:  [[ 2.87738580e-01 -1.64289178e+00  1.74713587e-04  1.46416301e-04
     2.60959893e+00]]
  Rotation vectors:  (array([[ 0.05661588],
         [-0.06887514],
         [-0.03784882]]), array([[-0.0115898 ],
         [-0.10066124],
         [-0.02593096]]), array([[ 0.18677958],
         [ 0.07713145],
         [-0.39083471]]), array([[ 0.04883779],
         [ 0.16379245],
         [-0.07388073]]), array([[-0.2543957 ],
         [-0.08430534],
         [-0.03456773]]), array([[-0.06215935],
         [ 0.23680063],
         [-0.38988796]]), array([[ 0.17659006],
         [-0.26566874],
         [-0.01166437]]), array([[ 0.23699089],
         [-0.13052591],
         [-0.01316686]]), array([[ 0.00220345],
         [-0.29225638],
         [ 0.0234284 ]]), array([[-0.14575027],
         [-0.30785823],
         [ 0.17841207]]))
  Translation vectors:  (array([[-2.88160559],
         [-3.82978407],
         [15.50593771]]), array([[-3.4330396 ],
         [-1.61083398],
         [10.54266537]]), array([[-3.48007969],
         [ 1.23969997],
         [12.20716971]]), array([[-3.46957103],
         [-1.16731658],
         [11.69662273]]), array([[-3.06211859],
         [-1.6459245 ],
         [ 9.95587667]]), array([[-3.94643561],
         [ 0.14085341],
         [11.55656299]]), array([[-1.30365844],
         [-0.57443397],
         [10.56071718]]), array([[-2.66640978],
         [-0.9829703 ],
         [10.64275398]]), array([[-1.52863813],
         [-1.42046782],
         [ 9.68438769]]), array([[-1.0763635 ],
         [-2.07618703],
         [ 9.62378177]]))
  ```

- 展示两张角点检测图

  <img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/results/corners_1.jpg" alt="corners_0" style="zoom:15%;" /><img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/results/corners_2.jpg" alt="corners_2" style="zoom:15%;" />



### 镜头畸变校正

- 核心代码如下

  ```python
  newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
  dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
  ```
  
- 右图为校正结果

  <img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/data/2.jpg" alt="1" style="zoom:15%;" /><img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/results/undistorted_2.jpg" alt="undistorted_2" style="zoom:18%;" />



### bev图获取

- 核心代码如下，获取鸟瞰图的transform后apply到图像

  ```python
  objp = np.float32([[0,0], [h-1,0], [0,w-1], [h-1,w-1]]) * 150
  imgp = np.float32([corners[0], corners[h-1], corners[-h], corners[-1]])
  H = cv2.getPerspectiveTransform(imgp, objp)
  bev = cv2.warpPerspective(img, H, img.shape[:2][::-1])
  ```
  
- 右图为bev图

  <img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/data/2.jpg" alt="1" style="zoom:15%;" /><img src="/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/hw3/results/bev_2.jpg" alt="bev_2" style="zoom:15%;" />