#coding:GBK


import warnings

warnings.filterwarnings("ignore")
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from urllib import request
import urllib.parse
from bs4 import BeautifulSoup as bs
import time
from math import ceil
import requests
import db
import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

domain='http://www.jjxsw.com'
img_folder='d:\\pythonproject\\test\\img\\'
novel_folder='d:\\pythonproject\\test\\novel\\'


# 获取小说详情地址列表,以及当前列表下一页地址
def getList(url):
    print('开始列表页分析，url:%s' %url)
    html_data=gethtml(url)
    soup = bs(html_data, 'html.parser')
    main_list = soup.find('div', id='catalog')
    main_list_item = main_list.find_all('div', class_='listbg')

    #获取详情url列表
    detailurl_list = []
    for value in main_list_item:
        url=makeurl(value.a['href'])
        detailurl_list.append(url)

    print(detailurl_list)
    #####这里处理小说详情，抓取数据
    for value in main_list_item:
        url=makeurl(value.a['href'])
        getnovel(url)

    ##返回下一列表的url
    next_url_a_list = soup.find('div',class_='pager').find_all('a')
    for value in next_url_a_list:
        if(value.string=='下一页'):
            url=makeurl(value.get('href'))
            return  url


###下载小说，小说入库   http://www.jjxsw.com/txt/22708.htm
def getnovel(url):
    no=int(ceil(time.time()*10000)) ##当前小说编号
    #小说详情页面
    html_data = gethtml(url)
    soup = bs(html_data, 'html.parser')
    downurl1 = soup.find_all('li', class_='downAddress_li')[0].find_all('a')[0].get('href')
    params=get_params(soup,no)
    print(params)
    db.connect(params)
    print('%s详情页面抓取完成' %no)
    # 下载页面

    downurl=makeurl(downurl1)
    download(downurl)

    print('%s小说下载完成' % no)

def gethtml(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)
        html_data = browser.page_source
    except BaseException:
        time.sleep(600)
        gethtml(url)
    else:
        return html_data

def get_params(soup,no):
    try:
        params=[]
        params.append('')  # id

        try:
            params.append(soup.find('div', id='downInfoArea').find('h1').string)  # title
        except BaseException:
            params.append('')

        try:
            params.append(re.sub(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', soup.find('div', id='mainSoftIntro').text))  # detail

            # params.append(soup.find('div', id='mainSoftIntro').get_text())  # detail
        except BaseException:
            params.append('')
        # imgurl=soup.find('div',class_='downInfoRowL').find('span',class_='img').find('img').get('src')
        # request.urlretrieve(imgurl, img_folder+'%s.jpg' % no)
        params.append(no)  # mainurl

        try:
            params.append(soup.find('div', id='path').find_all('a')[1].string)  # cat
        except BaseException:
            params.append('')

        try:
            params.append(soup.find('li', class_='zuozhe').find('a').get('title'))  # author
        except BaseException:
            params.append('')

        params.append(no)  # no

    except BaseException:
        pass
    else:
        return params
#下载小说
def download(url='http://www.jjxsw.com/txt/dl-49-23784.html'):
    try:
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': novel_folder}
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome('D:\\pythonproject\\test\\chromedriver.exe', chrome_options=options)
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="Frame"]/table/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/a[3]').click()
        time.sleep(15)
        driver.quit()
    except BaseException:
        pass

#处理url是否带前缀
def makeurl(url):
    made=re.match('http://', url)
    if(made!=None):
        return url
    else:
        return domain+url

def run(url):
    while True:
        url=getList(url)
        if(url==None):
            continue

#http://www.jjxsw.com/txt/Chuanyue/  1
#http://www.jjxsw.com/txt/chongshengxiaoshuo/    1
#http://www.jjxsw.com/txt/Lsjs/     1
#http://www.jjxsw.com/txt/Qinggan/  1
#http://www.jjxsw.com/txt/Young/      1
#http://www.jjxsw.com/txt/Wuxia/    1
#http://www.jjxsw.com/txt/tongrenxiaoshuo/
#http://www.jjxsw.com/txt/Juben/
#http://www.jjxsw.com/txt/dmtr/
#http://www.jjxsw.com/txt/Xuanhuan/
#http://www.jjxsw.com/txt/dushi/
#http://www.jjxsw.com/txt/tiexue/   1
#http://www.jjxsw.com/txt/Kongbu/
run('http://www.jjxsw.com/txt/tiexue/index_3.html')
# getnovel('http://www.jjxsw.com/txt/18647.htm')
