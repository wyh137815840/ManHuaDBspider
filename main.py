import spider
from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool
def index(url):
    print('正在下载,技术有限,本软件没有进度条,请耐心等候.')
    html= requests.get(url).content
    soup = BeautifulSoup(html,'lxml')
    title=soup.find('h1',{'class','comic-title'}).string
    type=[]
    type_t=(soup.find('ul',{'class','nav nav-tabs mx-1 mb-3'})).find_all('li')
    for t in type_t:
        type.append(t.find('a').string)
    rs=[] # 单行本,话名,话url
    ol=soup.find_all('ol',{'class','links-of-books num_div'})
    for i in range(0,len(ol)):
        li=[]
        li=ol[i].find_all('li')
        data2=[]
        for j in range(0,len(li)):
            data1 = []
            href=li[j].find('a').get('href')
            hua=li[j].find('a').get('title')
            data1.append(href)      #0
            data1.append(title)     #1
            data1.append(type[i])   #2
            data1.append(hua)       #3
            data1.append(j+1)
            data2.append(data1)
        rs.append(data2)
    print('漫画主页已读取完成')
    pool1=Pool(len(rs))
    pool1.map(type_down,rs)
    #for r in rs:
     #   type_down(r)

def type_down(data):
    for d in data:
    #for i in range(1,len(data)):
        try:
            spider.down_hua(d)
            print(d[3]+'下载完成')
        except:
            print(d[3] + '网站内容缺失,无法下载')
    #pool2 = Pool(3)
    #pool2.map(spider.down_hua, data)
def main():
    while 1:
        print('1.根据网址下载')
        print("2.搜索")
        choose=int(input("选择模式 :"))
        if(choose==1):
            url=input("请输入要下载的漫画的网址:")
            spider.index(url)
        elif(choose==2):
            spider.index(spider.search())
        else:
            print('你隔着乱打啥呢(只能输入1或2)')

def get_proxy1():
    return requests.get("http://home.wyh2019.club:5010/get/").json()
if __name__ == '__main__':
    # main()
    #print(get_proxy1())
    #print(2%2)
    html=requests.get('http://www.xbiquge.la/0/10/7109.html').content
    soup=BeautifulSoup(html,'lxml')
    print(soup)
    print('End')