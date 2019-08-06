#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import time


def find_image_url(url):
    t = urllib.splitquery(url)  # 把查询字符串分离出来
    if len(t) == 2:
        attrs = t[1].split("&")  # 由&分割
        key = 'mediaurl'
        for attr in attrs:
            (attr_key, attr_val) = urllib.splitvalue(attr)  # 分离键值
            if attr_key == key:
                img_url = urllib.unquote(attr_val)  # 获得图片的URL
                return img_url
    return None


def crawler_bing_picture(num_imgs, query, folder):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    path = './' + folder  # 用于保存下载图片的目录
    if not os.path.exists(path):  # 目录不存在，创建
        os.mkdir(path)

    num = 0
    first = 1
    while num <= num_imgs:  # 还没有下载到指定的数目的图片，继续
        try:
            url = 'http://cn.bing.com/images/search?{0}&first={1}'.format(
                urllib.urlencode({'q': query.encode('utf-8')}), first)  # 搜索到的图片的页面
            req = urllib2.Request(url, headers=headers)  # 创建请求
            web = urllib2.urlopen(req)  # 请求网页
            html_code = web.read().decode('utf-8')  # 读取HTML
            soup = BeautifulSoup(html_code, 'lxml')  # 放入BeautifulSoup
            img_divs = soup.select('div[class="imgpt"] > a')  # 找到图片所在的标签
            if len(img_divs) > 0:  # 如果找到图片标签
                url_base = 'http://cn.bing.com'  # 图片跳转链接的前一截
                for img_div in img_divs:
                    first += 1
                    url_img_web = url_base + img_div['href']  # 拼接图片单独显示的页面的URL
                    img_url = find_image_url(url_img_web)  # 从单独显示页面URL中分离出图片下载所在URL
                    if img_url is not None:  # 如果分离出正确的URL
                        print img_url
                        img_name = img_url.split('/')[-1]  # 取出图片名
                        save_path = path + '/' + img_name  # 保存的路径
                        try:
                            urllib.urlretrieve(img_url, save_path)  # 下载图片
                            print u'保存图片第{0}张图片：{1}'.format(num+1, save_path)
                            num += 1
                        except:
                            print u'下载图片出错'
                            continue
                        time.sleep(1)  # 睡眠1秒
        except:
            print u'爬取' + url + u'出错!'
            continue


if __name__ == '__main__':
    crawler_bing_picture(20, u'猪', 'Zhu')
