import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch


class EigenX():
    def __init__(self, num_imgs=50, img_shape=None, output_path='./results'):
        """
            img_shape: [height, width]
        """
        self.num_imgs = num_imgs
        self.img_shape = img_shape

        os.makedirs(output_path, exist_ok=True)
        self.output_path = output_path

    def read_image(self, dataset_path, random=False):
        if random:
            pass  # TODO
        else:
            img_name_list = os.listdir(dataset_path)[:self.num_imgs]
        img_list = [
            cv2.imread(os.path.join(dataset_path, i)) for i in img_name_list
        ]
        if self.img_shape is not None:
            self.img_list = [
                cv2.resize(img, self.img_shape) for img in img_list
            ]
        else:
            self.img_shape = img_list[0].shape
            self.img_list = img_list

        return self.img_list

    def train(self, p=0.5):
        # 1. Get average image
        vec_array = np.array([self.img2vec(img) for img in self.img_list])
        avg_vec = np.mean(vec_array, axis=0)
        avg_img = avg_vec.reshape(self.img_shape[:2])
        avg_img_path = os.path.join(self.output_path, 'avg_img.png')
        cv2.imwrite(avg_img_path, avg_img.astype('uint8'))

        # 2. Get eigenvectors using SVD
        vec_norm = torch.tensor(vec_array - avg_vec).cuda()
        u, s, v = torch.linalg.svd(vec_norm)
        eigenvecs = v.cpu().numpy()[:int(p * len(s))]

        # 3. Plot top 10 eigenvectors
        plt.figure()
        for i in range(10):
            plot_i = eigenvecs[i].reshape(self.img_shape)
            cv2.normalize(plot_i, plot_i, 0, 255, cv2.NORM_MINMAX)
            plt.subplot(2, 5, i + 1)
            plt.imshow(plot_i.astype('uint8'), cmap=plt.cm.gray)
            plt.xticks(())
            plt.yticks(())
            plt.title(f'{i+1}')

        plot_path = os.path.join(self.output_path, 'eigen_imgs_10.png')
        plt.savefig(plot_path)

        # 4. Restore some values for reconstruction
        v_path = os.path.join(self.output_path, f'v_{int(p*len(s))}.npy')
        np.save(v_path, eigenvecs)

        self.avg_vec = torch.tensor(avg_vec).cuda()
        self.avg_img = torch.tensor(avg_img).cuda()
        self.u = u
        self.v = v

    def reconstruct(self, img_path, nums_pc=[10, 25, 50, 75]):
        img = cv2.imread(img_path)
        if self.img_shape is not None:
            img = cv2.resize(img, self.img_shape)
        vec = (torch.tensor(self.img2vec(img)).cuda() -
               self.avg_vec).unsqueeze(0)  # [1, h*w]

        plt.figure()
        for i, k in enumerate(nums_pc):
            v_k = self.v[:, :k]
            vec_encode = torch.einsum('mn,nk -> mk', vec, v_k)
            vec_decode = torch.einsum('mk,kn -> mn', vec_encode, v_k.T)

            img_recon = (vec_decode + self.avg_vec).cpu().numpy().reshape(
                self.img_shape)
            cv2.normalize(img_recon, img_recon, 0, 255, cv2.NORM_MINMAX)

            plt.subplot(2, int((len(nums_pc) + 1) / 2), i + 1)
            plt.imshow(img_recon.astype('uint8'), cmap=plt.cm.gray)
            plt.xticks(())
            plt.yticks(())
            plt.title(f'{k}')
        img_name = img_path.split('/')[-1].split('.')[0]
        plt.savefig(f'./results/{img_name}_recon.jpg')

    @staticmethod
    def img2vec(img):
        vec = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)).flatten()
        return vec


if __name__ == '__main__':
    x = EigenX(num_imgs=200, img_shape=[100, 100], output_path='./results')
    """ Read images """
    dataset_path = './data/fullbody_anime_girls/ganime_fullbody_ultraclean_256/ \
                    resized_ganime_fullbody_ultraclean-20220708T155251Z-002/ \
                    resized_ganime_fullbody_ultraclean'

    x.read_image(dataset_path)
    """ Train """
    x.train(p=1)
    """ Reconstruct """
    for i in range(1, 4):
        img_path = f'./examples/{i}.jpg'
        x.reconstruct(img_path,
                      nums_pc=[10, 25, 50, 75, 100, 200, 300, 400, 500, 600])
