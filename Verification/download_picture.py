# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import urllib

"""
用于爬取训练所需的图片
爬取网站是网易邮箱的登陆页面
"""

driver = webdriver.Chrome()

driver.get("http://reg.163.com/")

for i in range(200):
    src_img = None
    print type(src_img)
    print "正在抓取的图片:\t%d"%i
    while not src_img:
        try:
            time.sleep(1)
            #进入iframe
            WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, 'zj-login')))
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
    path_img = r'../pic/yidun_img_%d.jpg'%i
    file_img = open(path_img, 'w b')
    file_img.write(data)
    file_img.close()

    driver.switch_to.default_content()
    driver.refresh()