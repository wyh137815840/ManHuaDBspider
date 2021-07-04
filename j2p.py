import os
import time
import requests
from fpdf import FPDF
from PIL import Image
def pdf(jpg_path,pdf_path):
    files = os.listdir(jpg_path)
    pngFiles = []
    filename_pdf = jpg_path.split('/')[-2]
    for file in files:
        pngFiles.append(jpg_path + file)
    im = Image.open(pngFiles[0])
    width, height = im.size
    pdf = FPDF(unit = "pt", format = [width, height])
    lenth=len(pngFiles)
    #i=1
    # imagelist is the list with all image filenames
    for image in pngFiles:
        pdf.add_page()
        pdf.image(image,x=0,y=0)
        #print('\r{0}/{1}  '.format(i,lenth), end='')
        #i=i+1
    #p=pdf_path+filename_pdf
    start = time.time();
    pdf.output(pdf_path+filename_pdf+".pdf", "F")
    end = time.time();
    D_time = int(end - start)
    str = filename_pdf+' done takes'+str(D_time)
    send_msg(str)
def send_msg(str):
    api = "https://sc.ftqq.com/SCU135617Te5a9a196461c20aa1038069205152c2a5fd8498b19f66.send"
    title = "通知"
    content = str
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(url=api, data=data)
if __name__ == '__main__':

    #p1='C:/Users/WYH.000/PycharmProjects/shenshimanga/1-第01话-我就叫刘忙/'
    #p2='C:/Users/WYH.000/PycharmProjects/shenshimanga/pfg/'
    #pdf(p1,p2)
    str='测试中,随便乱搭的'
    send_msg(str)