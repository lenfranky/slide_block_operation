# -*- coding:utf-8 -*-

from PIL import Image
import sys
import pic_sim
import os
import cv2

"""
检验图片分割、合成之后的效果
方法为用其所属于的聚类中的所有图片分别与其做相似性检测
"""

def verify_pic(path_root=r'../pic'):
    path_result = path_root + r'/result/result.jpg'
    path_cluster = path_root + r'/pic_cluster/cluster_0'

    pic_result = cv2.imread(path_result)

    # path_cluster = path_root + r'/pic_cluster'
    path_pic_current = path_cluster + r'/pic_0.jpg'
    pic_current = cv2.imread(path_pic_current)

    num_current = 0
    while not (pic_current is None):
        sim_value = pic_sim.mean_hash(path_result, path_pic_current)
        # print sim_value
        if sim_value > 10:
            print "不相似！"
        else:
            print "相似！"

        num_current += 1
        path_pic_current = path_cluster + r'/pic_%d.jpg' % num_current
        pic_current = cv2.imread(path_pic_current)

if __name__ == '__main__':
    verify_pic()