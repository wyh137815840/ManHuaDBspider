# -*- coding: utf-8 -*-
import time

import pymysql
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
from multiprocessing.dummy import Pool
import os
from fake_useragent import UserAgent
import base64
R_url='www.manhuadb.com'
img_host="https://i2.manhuadb.com"
home_path='H:/漫画/'
#home_path='../漫画/'
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
def get_img_data(soup):
    script=soup.find_all('script')
    return ((((script[8].string).replace('var img_data = ','')).replace("'",'')).replace(';',''))
def search():
 while 1:
    key=input('请输入漫画标题的关键字:')
    url='https://www.manhuadb.com/search?q={}'.format(key)
    html=requests.post(url).content
    soup=BeautifulSoup(html,'lxml')
    rs=BeautifulSoup(str(soup.find_all('div',{'class':'row m-0'})[0]).split('<!--翻页-->')[0],'lxml')
    div=rs.find_all('div',{'class':'col-4 col-sm-2 col-xl-1 px-1 px-md-1 px-lg-2 px-xl-1 pb-3'})
    li=[]
    for d in div:
        rs=[]
        tmp=d.find_all('a')
        rs.append(tmp[1].string)
        rs.append(tmp[2].string)
        rs.append(tmp[1].get('href'))
        li.append(rs)
    i=1
    for l in li:
        print(i,l[0],l[1])
        i=i+1
    choose=input('请根据需要输入选择:')
    if (int(choose) == 0):
        break
    elif(int(choose)<=len(li) and int(choose) > 0):
        d=li[int(choose)-1]
        h=d[2]
        href='https://'+R_url+h
        return href
def test():
    url='https://www.manhuadb.com/manhua/121/64_685.html'
    html = requests.post(url).content
    soup = BeautifulSoup(html, 'lxml')
    div=soup.find('div',{'class':'d-none vg-r-data'}).get('data-total')
    print(div)
def zfill(str):
    return '%05d' % str
def down_hua(data):
    url='https://www.manhuadb.com'+data[0]
    title = data[1]
    type=data[2]
    hua=data[3]
    hua_num=zfill(data[4])
    html = requests.post(url).content
    soup = BeautifulSoup(html, 'lxml')
    vg_r_data=soup.find('div',{'class':'d-none vg-r-data'})
    img_pre=vg_r_data.get('data-img_pre')
    img_data=get_img_data(soup)
    img_arr=D_BASE64(img_data)
    img_list=eval(img_arr)
    #print(type+hua+'解析完毕')
    p_data = []
    i=1
    for l in img_list:
        data=[]
        href=[]
        href.append(img_host+img_pre+l.get('img'))
        try:
            href.append(img_host+img_pre+l.get('img_webp'))
        except:
            print("\r",end=" ")
        data.append(href)
        data.append(title)
        data.append(type)
        data.append(hua)
        data.append(i)
        data.append(hua_num)
        p_data.append(data)
        i=i+1

    max=20
    pool2=Pool(max)
    pool2.map(save,p_data)
    #for p in p_data:
       # save(p)
def save(p_data):
    url=p_data[0]       #图片地址的数组
    url_jpg=url[0]      #获取img的地址
    title = p_data[1]   #获取漫画标题
    type=p_data[2]      #图片对应的漫画类别
    hua=p_data[3]       #图片对应的话
    page=zfill(p_data[4])     #图片对应的页码
    hua_num=p_data[5]   #话的序号

    path = home_path + title + '/' + type + '/' + str(hua_num)+'-'+hua + '/'  #图片存储的路径
    try:
        if not os.path.exists(path):#如果路径不存在,就新建
            os.makedirs(path)
    except:
        j=0
        j=j+1   #这两句无意义,只是创建路径有时候报错,为了程序流畅运行加的
    try:
        store_path = path +hua_num+'-'+ str(page) + '.'+getJPGorPNG(url_jpg)#图片的路径  getJPGorPNG是获取图片的后缀名
        response = requests.get(url_jpg)
        img = Image.open(BytesIO(response.content))
        img = img.save(store_path)   #保存图片
    except:
        url_webp = url[1]  #如果图片地址不是img,就是用img_webp的地址
        store_path = path +hua_num+'-'+str(page) + '.webp'
        response = requests.get(url_webp)
        img = Image.open(BytesIO(response.content))
        img = img.save(store_path)
def getJPGorPNG(url):
    return (url.split('/')[-1]).split('.')[-1]
def insert_manhuaDB_list(title,href):
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """
    insert into manhuaDB_list(title,url) value(%s,%s)
    """
    try:
        # 执行sql语句
        cursor.execute(sql,(title,'https://www.manhuadb.com'+href))
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def get_all_manga_list():
    #for i in range(1,501):
    for i in range(1, 501):
        print(i)
        url='https://www.manhuadb.com/manhua/list-page-{}.html'.format(str(i))
        html = requests.post(url).content
        soup = BeautifulSoup(html, 'lxml')
        div=soup.find_all('div',{'class':'media comic-book-unit'})
        for d in div:
            media_box=d.find('div',{'class','media-body'})
            h2=media_box.find('h2',{'class','h3 my-0'})
            a=h2.find('a')
            href=a.get('href')
            title=a.string
            insert_manhuaDB_list(title,href)
def get_10_record():
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cur = con.cursor()
    sql = 'select url from manhuaDB_list LIMIT 0,10'
    cursor = cur.execute(sql)
    result = cur.fetchall()
    href = []
    for h in result:
        href.append(h[0])
    cur.close()
    con.close()
    return href
def type_down(data):
    #for d in data:
    #for i in range(1,len(data)):
    try:
        size=len(data)
        if(size==1):
            max=1
        elif size<=5:
            max=2
        elif size<=20:
            max=5
        elif size>20:
            max=int(size/4)
        pool2 = Pool(max)
        pool2.map(do_down_hua, data)
    except:
        print('没有数据')
def do_down_hua(d):

    try:
        print(d[2] + d[3] + '开始下载')
        down_hua(d)
        print(d[2] + d[3] + '下载完成')
        return
    except:
        print(d[2] + d[3] + '网站顶不住了,无法下载')

def index(url):
    headers = {
        'Referer': 'http://www.manhuadb.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.manhuadb.com',
    }
    html= requests.get(url,headers).content
    soup = BeautifulSoup(html,'lxml')
    try:
        title=soup.find('h1',{'class','comic-title'}).string
        type = []
        type_t = (soup.find('ul', {'class', 'nav nav-tabs mx-1 mb-3'})).find_all('li')
        for t in type_t:
            type.append(t.find('a').string)
        rs = []  # 单行本,话名,话url
        ol = soup.find_all('ol', {'class', 'links-of-books num_div'})
        for i in range(0, len(ol)):
            li = []
            li = ol[i].find_all('li')
            data2 = []
            for j in range(0, len(li)):
                data1 = []
                href = li[j].find('a').get('href')
                hua = li[j].find('a').get('title')
                data1.append(href)  # 0
                data1.append(title)  # 1
                data1.append(type[i])  # 2
                data1.append(hua)  # 3
                data1.append(j + 1)
                data2.append(data1)
            rs.append(data2)
        print('漫画主页已读取完成')
        pool1 = Pool(len(rs))
        pool1.map(type_down, rs)
        #for r in rs:
        #    type_down(r)
            #delect_record(url)
    except:
        print('漫画不存在'+url)

    #pool1=Pool(len(rs))
    #pool1.map(type_down,rs)
def delect_record(url):
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cur = con.cursor()
    sql = "DELETE FROM manhuaDB_list WHERE url ='{}'".format(url)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交修改
        con.commit()
        print("delete OK")
    except:
        # 发生错误时回滚
        con.rollback()
    # 关闭连接
    con.close()
def down_all_manga():
    list=get_10_record()
    pool1=Pool(5)
    pool1.map(index,list)
def main():
    for i in range(0,20):
        print('第 '+str(i+1)+'个任务')
        down_all_manga()
    print('全部完成')
if __name__ == '__main__':
    #url='https://www.manhuadb.com/manhua/24490'
    #index(url)
    url='https://www.kuaikanmanhua.com/web/comic/320048/'
    html=requests.get(url).content
    soup=BeautifulSoup(html,'lxml')
    print(soup)
