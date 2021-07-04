import os
import time
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import requests
from numpy import long

import DBtools
import pypinyin
from PIL import Image
from io import BytesIO
import base64
import sys
#homepath='Z:/WEB/wwwroot/home.wyh2019.club/public/static/upload/book/'
homepath='./XWX/'
img_host="https://i2.manhuadb.com"
def Transpinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s =s+ ''.join(i)
    return s
def taglistTotags(list):
    tag=''
    for l in list:
        tag=tag+l+'|'
    return tag[:-1]
def saveCover(title,picurl):
    id=DBtools.get_bookID(title)
    path=homepath+str(id)+'/'
    if not os.path.exists(path):  # 如果路径不存在,就新建
        os.makedirs(path)
    store_path = path + 'cover.jpg'
    response = requests.get(picurl)
    img = Image.open(BytesIO(response.content))
    img = img.save(store_path)
def get_img_data(soup):
    script=soup.find_all('script')
    return ((((script[8].string).replace('var img_data = ','')).replace("'",'')).replace(';',''))
def D_BASE64(data):
    #base64 decode should meet the padding rules
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    dStr = base64.b64decode(data).decode()
    return dStr
def down_hua(data):
    hou=data[0]
    url='https://www.manhuadb.com'+hou
    title = data[1]
    hua=data[2]
    hua_num=data[3]
    html = requests.post(url).content
    soup = BeautifulSoup(html, 'lxml')
    vg_r_data=soup.find('div',{'class':'d-none vg-r-data'})
    img_pre=vg_r_data.get('data-img_pre')
    img_data=get_img_data(soup)
    img_arr=D_BASE64(img_data)
    img_list=eval(img_arr)
    #print(type+hua+'解析完毕')
    book_id=DBtools.get_bookID(title)
    DBtools.insert_chapter(book_id,hua,hua_num)
    chapter_id=DBtools.get_chapterID(book_id,hua_num)
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
        data.append(href)                       #图片链接
        data.append(DBtools.get_bookID(title))  #漫画id
        #data.append(type)
        data.append(hua)                        #话名
        data.append(chapter_id)                    #话编号
        data.append(i)                          #页码
        p_data.append(data)
        i=i+1
    max=5
    pool2=Pool(max)
    pool2.map(save,p_data)
    #for p in p_data:
        #save(p)
def save(p_data):
    url=p_data[0]       #图片地址的数组
    url_jpg=url[0]      #获取img的地址
    title_id = p_data[1]   #获取漫画标题的ID
    #type=p_data[2]      #图片对应的漫画类别
    hua=p_data[2]       #图片对应的话
    hua_num=p_data[3]   #话编号
    page=p_data[4]      #图片对应的页码

    path = homepath + str(title_id) + '/'+str(hua_num)+ '/'   #图片存储的路径
    try:
        if not os.path.exists(path):#如果路径不存在,就新建
            os.makedirs(path)
    except:
        j=0
        j=j+1   #这两句无意义,只是创建路径有时候报错,为了程序流畅运行加的
    try:
        #DBtools.insert_photo(hua_num, page)
        #pic_id=DBtools.get_pic_id(hua_num,page)
        #store_path = path + str(pic_id) + '.'+getJPGorPNG(url_jpg)#图片的路径  getJPGorPNG是获取图片的后缀名
        response = requests.get(url_jpg)
        #img = Image.open(BytesIO(response.content))
        #img = img.save(store_path)   #保存图片
        #DBtools.insert_photo(hua_num,page)
        DBtools.insert_photo_url(hua_num,page,url_jpg)
    except:
        url_webp = url[1]  #如果图片地址不是img,就是用img_webp的地址
        #pic_id = DBtools.get_pic_id(hua_num, page)
        #store_path = path + str(pic_id) + '.jpg'
        response = requests.get(url_webp)
        #img = Image.open(BytesIO(response.content))
        #img = img.save(store_path)
        #DBtools.insert_photo(hua_num,page)
        DBtools.insert_photo_url(hua_num,page,url_webp)
def getJPGorPNG(url):
    return (url.split('/')[-1]).split('.')[-1]
def get_mangainfo(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', {'class', 'comic-title'}).string
    tag_list_li = soup.find('ul', {'class', 'tags'}).find_all('li')
    tag_list=[]
    type=tag_list_li[0].find('a').string
    if(type=='连载中'):
        end=0
    else:
        end=1
    for i in range(1,len(tag_list_li)):
        tag_list.append(tag_list_li[i].find('a').string)
    summary = (soup.find('p', {'class', 'comic_story'}).string).replace('在漫画DB','在WYHmanhua')
    tags = taglistTotags(tag_list)
    pinyin = Transpinyin(title)

    img = soup.find('td', {'class', 'comic-cover'}).find('img').get('src')
    update_time=int(time.time())
    DBtools.insert_book_info(title, pinyin, tags, summary, end,img,update_time)
    #saveCover(title, img)
    rs = []  # 单行本,话名,话url
    ol = soup.find_all('ol', {'class', 'links-of-books num_div'})
    li = []
    li = ol[0].find_all('li')
    data = []
    for j in range(0, len(li)):
            data1 = []
            href = li[j].find('a').get('href')
            hua = li[j].find('a').string
            data1.append(href)  # 话的链接
            data1.append(title)  # 漫画标题
            #data1.append(type[i])  # 漫画的类别
            data1.append(hua)  # 话的名字
            data1.append(j + 1)  # 话的编号
            data.append(data1)


    #for d in data:
        #down_hua(d)
    pool1=Pool(3)
    pool1.map(do_down_hua,data)
def do_down_hua(d):
    try:
        down_hua(d)
    except:
        print(d[0])
if __name__ == '__main__':
   url='https://service-ir0hkdzh-1259447300.sh.apigw.tencentcs.com/release/manhua_chapter'
   body={
       url:'https://www.manhuadb.com/manhua/1488/1652_17519.html'
   }
   html=requests.post(url=url,body=body).content
   print(html)