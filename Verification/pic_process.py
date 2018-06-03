# -*- coding:utf-8 -*-

import sys
import os
import cv2
import code.pic_sim
from PIL import Image
from PIL import ImageChops
import numpy as np
import matplotlib.pyplot as plt

class Pic_Process(object):
    def __init__(self,
                 path_pic=r'../pic/origin/yidun_img_0.jpg',
                 path_cluster_folder=r'../pic/cluster_result',
                 path_pic_processed_folder=r'../pic/pic_processed/'):
        self.path_pic = path_pic
        self.path_cluster_folder = path_cluster_folder
        self.path_pic_processed_folder = path_pic_processed_folder
        self.path_cluster_pic = r''

        self.find_cluster()
        self.img_breach = self.find_breach()
        self.img_binary = self.get_img_binary()

    def find_cluster(self):

        num_pic_to_com = 0
        flag_find_cluster = False
        path_pic_to_com = self.path_cluster_folder + r'/cluster_%d.jpg' % num_pic_to_com
        pic_to_com = cv2.imread(path_pic_to_com)
        while not (pic_to_com is None):
            sim_value = code.pic_sim.mean_hash(self.path_pic, path_pic_to_com)
            # print 'sim_value: \t' + str(sim_value)
            if sim_value < 10:
                # print "find one same cluster"
                # print "属于的聚类:" + str(num_pic_to_com)
                flag_find_cluster = True
                break

            # 读取下一张图片
            num_pic_to_com += 1
            path_pic_to_com = self.path_cluster_folder + r'/cluster_%d.jpg' % num_pic_to_com
            pic_to_com = cv2.imread(path_pic_to_com)

        if flag_find_cluster:
           self.path_cluster_pic = path_pic_to_com
        else:
            print "未找到所属的分类！"

    def find_breach(self):
        img = Image.open(self.path_cluster_pic)
        img_cluster = Image.open(self.path_pic)
        img_breach = ImageChops.difference(img, img_cluster)
        img_breach.save(self.path_pic_processed_folder + r'breach.jpg')
        # self.img_breach = img_breach
        return img_breach

    def get_img_binary(self):

        #  convert to grey level image
        img = self.img_breach.convert('L')
        img.save(self.path_pic_processed_folder + 'breach_grey.jpg')

        #  setup a converting table with constant threshold
        threshold = 30
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        #  convert to binary image by the table
        img = img.point(table, '1' )

        img.save(self.path_pic_processed_folder + 'breach_binary.jpg')
        # self.img_binary = img
        return img

    def get_x(self):
        threshold_breach = 25

        width = self.img_binary.size[0]
        height = self.img_binary.size[1]

        img = np.array(Image.open(self.path_pic_processed_folder + r'breach_binary.jpg'))  # 打开图像并转化为数字矩阵

        # print img.shape
        # print img.dtype
        # print img.size
        # print type(img)

        breach_col_list = []
        for col in range(480):
            count = 0
            for row in range(240):
                if img[row][col] > 0:
                    count += 1
            breach_col_list.append(count)

        # print breach_col_list

        # count = 0
        x = 0
        # 连续三列的点的数量大于阈值则认为已经找到了缺口的开始位置
        flag_found_x = False
        flag_found_first_x = False
        flag_found_second_x = False
        for col in range(len(breach_col_list)):
            value_now = breach_col_list[col]
            if flag_found_second_x:
                if value_now > threshold_breach:
                    flag_found_x = True
                    break
                else:
                    flag_found_second_x = False
                    flag_found_first_x = False
            elif flag_found_first_x:
                if value_now > threshold_breach:
                    flag_found_second_x = True
                else:
                    flag_found_first_x =False
            else:
                if value_now > threshold_breach:
                    flag_found_first_x = True
                x = col

        if flag_found_x:
            # print "开始位置：\t" + str(x)
            return x
        else:
            print "未找到开始位置"


if __name__ == '__main__':
    pic = Pic_Process(path_pic=r'../pic/origin/yidun_img_5.jpg')
    x = pic.get_x()
