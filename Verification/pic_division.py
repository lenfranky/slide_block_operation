# -*- coding:utf-8 -*-

from PIL import Image
import sys


def fill_image(image):
    width, height = image.size
    print(width, height)

    new_image_length = width if width > height else height

    print(new_image_length)

    # new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
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


def save_images(image_list):
    index = 1
    for image in image_list:
        image.save(r'../pic/result/' + str(index) + r'.png')
        index += 1


if __name__ == '__main__':
    file_path = "yidun_img_0.jpg"
    # 打开图像
    image = Image.open(file_path)
    # 将图像转为正方形，不够的地方补充为白色底色
    image = fill_image(image)
    # 分为图像
    image_list = cut_image(image)
    # 保存图像
    save_images(image_list)