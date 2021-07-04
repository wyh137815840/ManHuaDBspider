from PIL import Image
import os
import PyPDF2
def combine2Pdf( folderPath, pdfFilePath ):
    files = os.listdir( folderPath )
    pngFiles = []
    sources = []
    for file in files:
            pngFiles.append( folderPath + file )
    pngFiles.sort()
    output = Image.open( pngFiles[0] )
    pngFiles.pop( 0 )
    for file in pngFiles:
        pngFile = Image.open( file )
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert( "RGB" )
        sources.append( pngFile )
    filename_pdf = folderPath.split('/')[-2]
    pdfFilePath=pdfFilePath+filename_pdf+'.pdf'
    output.save( pdfFilePath, "pdf", save_all=True, append_images=sources )
def pdf_combin(dir):
    files = os.listdir(dir)
    filenames=[]
    for f in files:
        filenames.append(dir+f)
    merger = PyPDF2.PdfFileMerger()
    for filename in filenames:
        merger.append(PyPDF2.PdfFileReader(filename))
    filename_pdf = dir.split('/')[-2]
    merger.write(filename_pdf+'.pdf')
def pdf():
    p = 'C:/Users/WYH.000/PycharmProjects/ManHuaDB/古风漫画/放开那个女巫/'
    files = os.listdir(p)
    for f in files:
        p1 = p + f + '/'
        p2 = 'C:/Users/WYH.000/PycharmProjects/ManHuaDB/古风漫画/PDF/'
        combine2Pdf(p1, p2)
def combin():
    pdf_combin('C:/Users/WYH.000/PycharmProjects/ManHuaDB/古风漫画/PDF/')
if __name__ == '__main__':
    combin()
    #pdf()