# image2Prompt2IMAGE: 以prompt为中介的本地图生图

## 背景

​	在进行图生图时，有时我们希望基于图片A的基本要素，创作多张包含这些要素而又全新的图片B。直接的图生图模型一般强依赖于原图A，较难满足这样的需求，一个很自然的想法是，将图片A的文字形式化为提示词A，将提示词A按意愿修改为提示词B，再用提示词B生成图片B，这样就能得到一张基于图片A要素的全新生成的图片B。

​	这个过程可以通过调用多模态大模型的API来解决，但网页端手工操作既麻烦，每次又只能处理一张图片；调用API一般需要花钱，得到OpenAI这类API也相对有一些门槛。而不过，这个过程完全可以用本地模型来免费完成：对于从图片A中提取提示词B这个过程，其本质上是一个图片描述任务，在前大模型时代就有很多做得较好的相关工作如CLIP；对于从提示词B中生成图片B这个过程，也可以下载然后调用本地的Pretrained Diffusion Model。这样我们就能得到一个本地的模型工作流，批量化免费地完成图生图的定制任务。



##  image2Prompt

​	我们使用CLIP model进行图片提示词提取。CLIP是一个前大模型时代的经典多模态模型，它由一个图像编码器和一个文本编码器组成，图像编码器负责将图像嵌入到语义空间中，而文本编码器则负责将文本嵌入到同样的语义空间中。CLIP模型使用了Transformer架构来实现这两个编码器，这种架构能够处理长距离的依赖关系，并且在大规模数据上进行预训练。

![CLIP](/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/final_project/imgs/CLIP.png)

​	我们使用了[ViT-H-14/laion2b_s32b_b79k](https://github.com/pharmapsychotic/clip-interrogator)版本，model weights已在链接中开源。



## Prompt2IMAGE

​	我们使用Stable Diffusion进行图片生成。Stable Diffusion模型整体上是一个End-to-End模型，主要由VAE，U-Net以及CLIP Text Encoder（也是CLIP :）三个核心组件构成。其中，VAE用于图像压缩和图像重建，CLIP用来提取文本的特征。U-Net模型是核心部分，用于预测噪声残差，并结合Sampling method对输入的特征矩阵进行重构，逐步将其从随机高斯噪声转化成图片的Latent Feature。

![Stable_Diffusion](/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/final_project/imgs/Stable_Diffusion.svg)

​	我们使用了[stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)](https://github.com/pharmapsychotic/clip-interrogator)版本，model weights已在链接中开源。



## 结果

- 原图

  ![zelda](/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/final_project/examples/zelda.png)

- 生成的prompt

  ```
  arafed view of a man standing on a rock with a sword and shield, nintendo clouds, sunset!, zelda and link, expansive cinematic view, clear skies in the distance, ruins in the background, textless, nintendo official media, ; wide shot, absolutely outstanding image
  ```

- 结果（生成15张，挑选了4张看起来较好的）

  ![results](/Users/jiahe/Documents/ZJU/CS/Courses/zjucs-graduate-courses/计算机视觉/final_project/imgs/results.png)



## 总结

过程中的几个感受：

1. CLIP作为image to prompt的工具还是挺不错的，它输出的prompt我觉得写的比我好且全面
2. 本地的小型stable diffusion确实不那么强，要真搞生成可用级别的图像还得依托midjourney这种云上的大diffusion
3. 之前一直没弄清楚stable diffusion在ddpm上加了什么东西，这次看了看学到了这个结构