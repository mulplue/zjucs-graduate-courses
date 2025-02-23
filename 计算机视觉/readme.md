- 这研究生课甚至是同名的本科生课青春版，抽象

1. hw1
   - cpp版本参考 https://github.com/WaveLong/ZJU-computer-vision/tree/master
   - python版本参考 https://github.com/Ryan-yang125/Computer-Vision
   - 参考了python版，简单封装了一下，有个简笔画的要求似乎不一样，换了个miku剪影

2. hw2
   - 数据集 https://www.kaggle.com/datasets/hirunkulphimsiri/fullbody-anime-girls-datasets
   - 一些preprocess参考 https://github.com/Ryan-yang125/Computer-Vision ，主要的修改是改用了svd，以及用torch加速并整理了code
   - 看起来EigenX里的X相当局限，大部分单object dataset都是多视角&物体形状diversity比较大的，人脸算是个比较特别的case，最后找了个full body的数据集，看着效果还可以
   - 感觉一个比较有意思的玩法是用generative model生成一大堆图片当dataset，然后看一下比如给decoder输一个0向量进去，出来时会不会和平均脸很像，以及看一下特征脸在latent space对应的值之类，不过没时间折腾

3. hw3
   - 经典的相机标定，流程都差不多，参考了 https://github.com/Nocami/PythonComputerVision-6-CameraCalibration
   - 理论上最好用正规的标定板，据说白色换成绿色还能提升精度，但我懒了，就直接在电脑上拍了

4. final project
   - 参考 https://zhuanlan.zhihu.com/p/619702740
   - 因为发布topic的时候说diffusion可以选择调调prompt，不用train，于是选了这个最省力的