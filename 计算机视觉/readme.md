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