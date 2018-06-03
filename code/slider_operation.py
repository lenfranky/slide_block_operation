# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import urllib


import code.pic_process
from selenium.webdriver.common.action_chains import ActionChains
import math

class Slider_Operation(object):
    def __init__(self, driver):
        if driver:
            self.driver = driver
        else:
            self.driver = webdriver.Chrome()

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = [0.0]
        # 当前位移
        current = 0.0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0.0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2.0
            else:
                # 加速度为负3
                a = -3.0
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 0.5 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            move = round(move)
            track.append(move)
        return track

    def get_track_2(self, distance):
        track_list = []
        dis = distance / 2
        track_0 = self.get_track(dis)
        for track in track_0:
            track_list.append(track)
        for i in range(len(track_0)):
            track_list.append(int(0))
        for track in track_0:
            track_list.append(track)

        return track_list

    def slide_slider_with_refreseh(self):
        driver = self.driver
        src_img = None
        while not src_img:
            try:
                # time.sleep(0.25)
                # 进入iframe
                WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'zj-login')))
                frame_father = driver.find_element_by_class_name('zj-login')
                # print"found zj-login!"
                iframe = frame_father.find_element_by_tag_name('iframe')
                # iframe = driver.find_element_by_xpath('//*[@id="x-URS-iframe1526110797407.0286"]')
                driver.switch_to_frame(iframe)  # 登录页面存在iframe
                WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))

                yidun_bg_img = driver.find_element_by_class_name('yidun_bg-img')
                src_img = yidun_bg_img.get_attribute('src')
                # print type(src_img)
                # driver.get(src_img)
                print "wait"
            except:
                driver.refresh()
                print "refreshed"

        fp = urllib.urlopen(src_img)
        data = fp.read()
        fp.close()
        path_img = r'../pic/yidun_img.jpg'
        file_img = open(path_img, 'w b')
        file_img.write(data)
        file_img.close()

        driver.switch_to.default_content()
        # driver.refresh()

        pic = code.pic_process.Pic_Process(path_pic=r'../pic/yidun_img.jpg',
                                           path_cluster_folder=r'../pic/cluster_result',
                                           path_pic_processed_folder=r'../pic/pic_processed/')
        x = pic.get_x()
        print "\t\t\t\t\t\t\t\t缺口的位置：\t" + str(x)

        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'zj-login')))
        frame_father = driver.find_element_by_class_name('zj-login')
        # print"found zj-login!"
        iframe = frame_father.find_element_by_tag_name('iframe')
        # iframe = driver.find_element_by_xpath('//*[@id="x-URS-iframe1526110797407.0286"]')
        driver.switch_to_frame(iframe)  # 登录页面存在iframe
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        slider = driver.find_element_by_class_name('yidun_slider')

        bar = driver.find_element_by_class_name('yidun_control')
        # print item.size
        # print slider.size
        bar_length = bar.size.get('width')
        # print bar_length

        x_to_move = int(x * bar_length / 480)
        # print "x_to_move:\t" + str(x_to_move)
        x_to_move += 10
        track_list = self.get_track(x_to_move)

        action = ActionChains(driver)
        action.click_and_hold(slider).perform()
        time.sleep(1)
        action.reset_actions()
        for track in track_list:
            action.move_by_offset(track, 0).perform()
            action.reset_actions()
        time.sleep(0.25)
        action.release().perform()
        action.reset_actions()

    def slide_slider(self):

        driver = self.driver
        """
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'zj-login')))
        frame_father = driver.find_element_by_class_name('zj-login')
        # print"found zj-login!"
        iframe = frame_father.find_element_by_tag_name('iframe')
        # iframe = driver.find_element_by_xpath('//*[@id="x-URS-iframe1526110797407.0286"]')
        driver.switch_to_frame(iframe)  # 登录页面存在iframe
        """
        WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))

        yidun_bg_img = driver.find_element_by_class_name('yidun_bg-img')
        src_img = yidun_bg_img.get_attribute('src')

        fp = urllib.urlopen(src_img)
        data = fp.read()
        fp.close()
        path_img = r'../pic/yidun_img.jpg'
        file_img = open(path_img, 'w b')
        file_img.write(data)
        file_img.close()

        driver.switch_to.default_content()
        # driver.refresh()

        pic = code.pic_process.Pic_Process(path_pic=r'../pic/yidun_img.jpg',
                                           path_cluster_folder=r'../pic/cluster_result',
                                           path_pic_processed_folder=r'../pic/pic_processed/')
        x = pic.get_x()
        # print x

        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'zj-login')))
        frame_father = driver.find_element_by_class_name('zj-login')
        # print"found zj-login!"
        iframe = frame_father.find_element_by_tag_name('iframe')
        # iframe = driver.find_element_by_xpath('//*[@id="x-URS-iframe1526110797407.0286"]')
        driver.switch_to_frame(iframe)  # 登录页面存在iframe
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        slider = driver.find_element_by_class_name('yidun_slider')

        bar = driver.find_element_by_class_name('yidun_control')
        # print item.size
        # print slider.size
        bar_length = bar.size.get('width')
        # print bar_length

        x_to_move = int(x * bar_length / 480)
        # print "x_to_move:\t" + str(x_to_move)
        x_to_move += 10
        track_list = self.get_track_2(x_to_move)

        action = ActionChains(driver)
        action.click_and_hold(slider).perform()
        time.sleep(1)
        action.reset_actions()
        for track in track_list:
            action.move_by_offset(track, 0).perform()
            action.reset_actions()
        time.sleep(0.25)
        action.release().perform()
        action.reset_actions()

        driver.switch_to.default_content()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://reg.163.com/")

    slider = Slider_Operation(driver)
    slider.slide_slider_with_refreseh()

    time.sleep(600)
    driver.close()
