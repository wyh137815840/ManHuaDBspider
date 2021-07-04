import re
import time

import pymysql
from bs4 import BeautifulSoup
import requests
import urllib3
from PIL import Image
from io import BytesIO
from multiprocessing.dummy import Pool
import os
import JPGtoPDF
host_url='https://www.gufengmh8.com'
host_path='./'
proxy={
    'http':'http://127.0.0.1:10809',
    'https':'https://127.0.0.1:10809'
}
def get_list(url):
    urllib3.disable_warnings()
    html=gethtml(url)
    soup=BeautifulSoup(html,'lxml')
    title=soup.find('div',{'class':'book-title'}).find('h1').string
    li=soup.find('ul',{'id':'chapter-list-1'}).find_all('li')
    main_d=[]
    for l in li:
        d=[]
        d.append(title)
        d.append(l)
        main_d.append(d)
    print('主页信息获取完成')
    pool1=Pool(20)
    pool1.map(hua_down,main_d)

    #for l in li:
        #hua_down(l)
def gethtml(url):
    i=1
    while 1:
        try:
            html = requests.get(url, timeout=60).content
            return html
        except requests.exceptions.RequestException:
            print('超时,刷新页面,这是第'+str(i)+'次刷新')
            i=i+1
def gethtml1(url,str):
    i=1
    while 1:
        try:
            html = requests.get(url, timeout=60).content
            return html
        except requests.exceptions.RequestException:
            if(i>2):
                print('超时,刷新页面,这是第'+str(i)+'次刷新 '+str)
            else:
                print('超时,刷新页面,这是第'+str(i)+'次刷新')
            i=i+1
def hua_down(d):
    title=d[0]
    l=d[1]
    url=host_url+l.find('a').get('href')
    hua=l.find('span').string.replace(' ','-')
    html=gethtml1(url,hua)
    soup=BeautifulSoup(html,'lxml')
    chapterImages=re.findall(".*chapterImages =(.*);var chapterPath.*", str(soup))[0]
    img_list=eval(chapterImages)
    img_pre=eval(re.findall(".*chapterPath = (.*);var pageTitle.*", str(soup))[0])
    img_host = 'https://res.xiaoqinre.com/'
    p_data=[]
    j=1
    for i in img_list:
        data=[]
        data.append(img_host+img_pre+i)
        data.append(title)
        data.append(hua)
        data.append(j)
        p_data.append(data)
        j=j+1
    pool2=Pool(20)
    pool2.map(save,p_data)
    p=host_path+'古风漫画/'+title+'/'+hua+'/'
    p1=host_path+'古风漫画/PDF/'
    #jpg2pdf.topdf(p, pictureType=['png', 'jpg'], save=p1)
    JPGtoPDF.combine2Pdf(p,p1)
    print(hua+'完成')
    #for p in p_data:
     #   save(p)
def yema(p):
    return '%04d' % p
def save(p_data):
    path=host_path+'古风漫画/'+p_data[1]+'/'+p_data[2]+'/'
    try:
        if not os.path.exists(path):  # 如果路径不存在,就新建
                os.makedirs(path)
    except:
        j=1+1
    store_path = path + yema(p_data[3]) + '.'+getJPGorPNG(p_data[0])  # 图片的路径  getJPGorPNG是获取图片的后缀名
    try:
        response = requests.get(p_data[0])
        img = Image.open(BytesIO(response.content))
        img = img.save(store_path)
    except:
        print(p_data[1]+p_data[2]+' '+str(p_data[3])+'图片不存在')
def getJPGorPNG(url):
    return (url.split('/')[-1]).split('.')[-1]
def main():
    url = 'https://www.gufengmh8.com/manhua/dushihuacongxiaoyaoyou/'
    start = time.time();
    get_list(url)
    end = time.time();
    D_time = end - start
    print("用时:" + str(D_time))
if __name__ == '__main__':
    main()