import pymysql
import main
def insert_ershou_url(id,h):
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='top',
        passwd='137815840',
        db='top',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """INSERT INTO ershou_url(id,url)
             VALUES ('{}','{}')""".format(id,h)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def insert_book_info(title,pinyin,tags,summary,ISend,cover,up_time):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """INSERT INTO xwx_book(unique_id,book_name,nick_name,tags,summary,area_id,is_copyright,end,author_id,cover_url,last_time)
             VALUES ('{}','{}','{}','{}','{}',{},{},{},{},'{}',{})""".format(pinyin,title,title,tags,summary,1,2,ISend,4,cover,up_time)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def insert_chapter(book_id,chapter_name,chapter_order):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """INSERT INTO xwx_chapter(book_id,chapter_name,chapter_order)
                 VALUES ({},'{}',{})""".format(int(book_id), chapter_name, chapter_order)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def insert_photo(chapter_id,pic_order):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """INSERT INTO xwx_photo(chapter_id,pic_order)
                 VALUES ({},{})""".format(chapter_id, pic_order)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def insert_photo_url(chapter_id,pic_order,url):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cursor = con.cursor()
    sql = """INSERT INTO xwx_photo(chapter_id,pic_order,img_url)
                 VALUES ({},{},'{}')""".format(chapter_id, pic_order,url)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    cursor.close()
    con.close()
def get_bookID(title):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cur = con.cursor()
    sql="select id from xwx_book where book_name='{}'".format(title)
    cursor = cur.execute(sql)
    result = cur.fetchall()
    for h in result:
        id=h[0]
    cur.close()
    con.close()
    return id
def get_chapterID(book_id,hua_num):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cur = con.cursor()
    sql = "select id from xwx_chapter where book_id={} and chapter_order={}".format(book_id,hua_num)
    cursor = cur.execute(sql)
    result = cur.fetchall()
    for h in result:
        id = h[0]
    cur.close()
    con.close()
    return id
def get_pic_id(chp_id,pic_order):
    con = pymysql.Connect(
        host='home.wyh2019.club',
        port=3307,
        user='comic',
        passwd='137815840',
        db='comic',
        charset='utf8'
    )
    cur = con.cursor()
    sql = "select id from xwx_photo where chapter_id={} and pic_order={}".format(chp_id, pic_order)
    cursor = cur.execute(sql)
    result = cur.fetchall()
    for h in result:
        id = h[0]
    cur.close()
    con.close()
    return id
def clear_done():
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='House',
        passwd='137815840',
        db='House',
        charset='utf8'
    )
    cur = con.cursor()
    sql = 'select url from ershou_info'
    cursor = cur.execute(sql)
    result = cur.fetchall()
    href = []
    for h in result:
        key=main.B_href(h[0])
        delect(key[0])
    print('删除完成!')
def delect(key):
    con = pymysql.Connect(
        host='server.wyh2019.club',
        port=3306,
        user='House',
        passwd='137815840',
        db='House',
        charset='utf8'
    )
    cur = con.cursor()
    sql="DELETE FROM ershou_url WHERE id ='{}'".format (key)
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
if __name__ == '__main__':
    clear_done()
