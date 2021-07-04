import json
import re
import execjs
import pymysql
from bs4 import BeautifulSoup
import requests
from PIL import Image
import json
from io import BytesIO
from multiprocessing.dummy import Pool
import os
from fake_useragent import UserAgent
import base64
def get_img_data_arr(img_data):
    decode_Rs=base64.b64decode(img_data)
    return decode_Rs
def D_BASE64(data):

    #base64 decode should meet the padding rules
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    dStr = base64.b64decode(data).decode()
    return dStr
def get_img_list(url):
    html = requests.post(url).content
    soup = BeautifulSoup(html, 'lxml')
    s=soup.find_all('script')
    print(s[12])
    img_data=(s[12].string.split(','))[0].split("'")[1]
    #get_img_data_arr(img_data)
    #img_arr = D_BASE64(img_data)
    #img_list = eval(img_arr)
    print(img_data)
def get_picture_data(data):
    url='https://m.mkzhan.com'+data[0]
    title=data[1]
    hua=data[2]
    html= requests.get(url).content
    soup=BeautifulSoup(html,'lxml')
    div=soup.find('ul',{'class':'comic-list'})
    li=div.find_all('li')
    p_data=[]
    i=1
    for dd in li:
        data=[]
        data.append(dd.find('img').get('src'))
        data.append(title)
        data.append(hua)
        data.append(i)
        i=i+1
    print(p_data)
def get_list(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    title=soup.find('p',{'class':'comic-title j-comic-title'}).string
    div = soup.find('div', {'class': 'chapter__list clearfix'})
    li=div.find_all('li')
    data=[]
    for l in li:
        d=[]
        h=l.find('a').get('data-hreflink')
        t=str(l.find('a'))
        try:
            t1 = re.findall(".*>(.*)</a>.*", t)
        except:
            t1 = re.findall(".*</i>(.*)</a>.*", t)
        d.append(h)
        d.append(title)
        d.append(str(t1).replace(' ',''))
        data.append(d)
    pool1=Pool(1)
    pool1.map(get_picture_data,data)
if __name__ == '__main__':
    url='https://www.mkzhan.com/49733/'
    get_list(url)
    a='</i>                      第873话 斗圣复活                    </a>'
    t1 = re.findall(".*>(.*)</a>.*", a)
    print(t1)
    #print(D_BASE64(d2))
