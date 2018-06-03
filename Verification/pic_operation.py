# -*- coding:utf-8 -*-

from PIL import Image
import sys
import os

def fill_image(image):
    width, height = image.size
    print(width, height)

    new_image = Image.new(image.mode, (width, height), color='white')

    new_image.paste(image, (0, 0))
    return new_image


def cut_image(image):
    width, height = image.size
    item_width = int(width / 2)
    item_height = int (height)
    box_list = []
    for i in range(2):
        box = (i * item_width, 0 * item_height, (i + 1) * item_width, 1 * item_height)
        box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def save_images(image_list, path_root=r'../pic/result/'):
    index = 1
    for image in image_list:
        image.save(path_root + str(index) + r'.jpg')
        index += 1


def save_images_left_right(image_list, path_root=r'../pic/result/', flag = 'left'):
    if flag == 'left':
        image_list[0].save(path_root + r'/left_part.jpg')
    elif flag == 'right':
        image_list[1].save(path_root + r'/right_part.jpg')

def pic_division(file_path = r"yidun_img_0.jpg", flag = 'left', path_out_put_folder=r''):
    # 打开图像
    image = Image.open(file_path)
    # 将图像转为正方形，不够的地方补充为白色底色
    image = fill_image(image)
    # 分为图像
    image_list = cut_image(image)
    # 保存图像
    save_images_left_right(image_list, path_out_put_folder, flag)

def pic_merge(path_read_folder=r'../pic/result', path_write_folder=r'', num_cluster=0):
    path_pic_left = path_read_folder + r'/left_part.jpg'
    path_pic_right = path_read_folder + r'/right_part.jpg'
    pic_left = Image.open(path_pic_left)
    pic_right = Image.open(path_pic_right)

    item_width, item_height = pic_left.size
    width = int(item_width * 2)
    height = item_height
    print(width, height)

    new_image = Image.new(pic_left.mode, (width, height), color='white')

    box_list = []

    for i in range(2):
        box = (i * item_width, 0 * item_height, (i + 1) * item_width, 1 * item_height)
        box_list.append(box)

    new_image.paste(pic_left, box_list[0])
    new_image.paste(pic_right, box_list[1])

    path_result = path_write_folder + r'/cluster_%d.jpg' % num_cluster
    new_image.save(path_result)

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

def process():
    num_cluster = 0
    path_cluster_folder = r'../pic/pic_cluster/cluster_%d' % num_cluster
    while judge_folder_exist(path_cluster_folder):
        path_right = path_cluster_folder + r'/left.jpg'
        path_left = path_cluster_folder + r'/right.jpg'

        pic_division(path_right, 'right', path_cluster_folder)
        pic_division(path_left, 'left', path_cluster_folder)

        # print num_cluster
        num_cluster += 1
        path_cluster_folder = r'../pic/pic_cluster/cluster_%d' % num_cluster
        print path_cluster_folder

    num_cluster = 0
    path_cluster_folder = r'../pic/pic_cluster/cluster_%d' % num_cluster
    while judge_folder_exist(path_cluster_folder):

        pic_merge(path_read_folder=path_cluster_folder,
                  path_write_folder=r'../pic/cluster_result',
                  num_cluster=num_cluster)

        # print num_cluster
        num_cluster += 1
        path_cluster_folder = r'../pic/pic_cluster/cluster_%d' % num_cluster
        print path_cluster_folder


if __name__ == '__main__':
    # pic_division(r"yidun_img_0.jpg")
    # pic_merge()
    process()