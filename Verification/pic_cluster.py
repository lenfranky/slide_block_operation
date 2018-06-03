# -*- coding:utf-8 -*-

import pic_sim
import os
import cv2
import numpy as np

# 由相对路径得到绝对路径
def get_path_abs(self, path_relative=r'../file_IO/excel_file.xls'):
    path_abs = os.path.abspath(path_relative)
    return path_abs

# 判断文件夹是否存在
def judge_folder_exist(path = r'../pic'):
    path_abs = get_path_abs(path)
    flag = os.path.exists(path)
    # print type(flag)
    # print flag
    return flag


def pic_find_cluster_pic():
    path_root = r'../pic'
    # path_cluster = []
    path_cluster = path_root + r'/pic_cluster'
    # path_cluster = r'../pic/pic_cluster'
    # path_cluster = get_path_abs(path_cluster)
    # print path_cluster
    pic_cluster_0_path = path_cluster + r'/pic_0.jpg'
    path_pic_current = path_root + r'/origin/yidun_img_0.jpg'
    pic_current = cv2.imread(path_pic_current)

    # 判断目前pic_cluster文件夹中是否有初始的图片
    # 若没有，则将第一张图片作为其中的第一张图片
    if not judge_folder_exist(pic_cluster_0_path):
        print 'creat first cluster!'
        cv2.imwrite(pic_cluster_0_path, pic_current)
    else:
        pass

    for i in range(320):
        path_pic_current = path_root + r'/origin/yidun_img_%d.jpg' % i
        pic_current = cv2.imread(path_pic_current)

        num_pic_to_com = 0
        flag_find_cluster = False
        path_pic_to_com = path_cluster + r'/pic_%d.jpg' % num_pic_to_com
        pic_to_com = cv2.imread(path_pic_to_com)
        while not (pic_to_com is None):
            sim_value = pic_sim.mean_hash(path_pic_current, path_pic_to_com)
            print 'sim_value: \t' + str(sim_value)
            if sim_value < 10:
                print "find one same cluster"
                flag_find_cluster = True
                break

            # 读取下一张图片
            num_pic_to_com += 1
            path_pic_to_com = path_cluster + r'/pic_%d.jpg' % num_pic_to_com
            pic_to_com = cv2.imread(path_pic_to_com)
            
        if flag_find_cluster:
            pass
        else:
            # print num_pic_to_com
            # print path_pic_to_com
            cv2.imwrite(path_pic_to_com, pic_current)

def pic_cluster():
    path_root = r'../pic'
    path_cluster = path_root + r'/pic_cluster'
    path_pic_current = path_root + r'/origin/yidun_img_0.jpg'
    pic_current = cv2.imread(path_pic_current)

    num_current = 0
    while not (pic_current is None):
        num_cluster = 0
        path_pic_cluster = path_cluster + r'/pic_%d.jpg' % num_cluster
        pic_cluster = cv2.imread(path_pic_cluster)
        while not (pic_cluster is None):
            sim_value = pic_sim.mean_hash(path_pic_current, path_pic_cluster)
            if sim_value < 10:
                break

            num_cluster += 1
            path_pic_cluster = path_cluster + r'/pic_%d.jpg' % num_cluster
            pic_cluster = cv2.imread(path_pic_cluster)


        num_in_cluter = 0
        path_pic_in_cluster = path_cluster + r'/cluster_%d/pic_%d.jpg' % (num_cluster,num_in_cluter)
        pic_in_cluster = cv2.imread(path_pic_in_cluster)
        while not (pic_in_cluster is None):
            num_in_cluter += 1
            path_pic_in_cluster = path_cluster + r'/cluster_%d/pic_%d.jpg' % (num_cluster, num_in_cluter)
            pic_in_cluster = cv2.imread(path_pic_in_cluster)

        path_write = path_pic_in_cluster
        print path_write
        cv2.imwrite(path_write, pic_current)

        num_current += 1
        path_pic_current = path_root + r'/origin/yidun_img_%d.jpg' % num_current
        pic_current = cv2.imread(path_pic_current)


if __name__ == '__main__':
    # pic_find_cluster_pic()
    pic_cluster()