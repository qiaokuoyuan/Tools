from bs4 import BeautifulSoup
from urllib import request
import re
import os
import pymysql
import time
import eventlet

STATIC_DB_NAME = "yiren"
STATIC_TABLE_NAME = "yiren_pic"
STATIC_PIC_SAVE_DIR = 'd:/d/yiren_pic/'

STATIC_HOST = 'http://www.yiren19.com'
STATIC_MYSQL_CON = pymysql.connect(host="127.0.0.1", user="root", password="root", db=STATIC_DB_NAME, charset="utf8")
STATIC_MYSQL_CUR = STATIC_MYSQL_CON.cursor()

ass = []


# 获得指定页面的html
def get_html(url):
    with eventlet.Timeout(60 * 5):
        print('get_html---->' + str(url))
        response = request.urlopen(url)
        html = response.read()
        return html


# 获得最后一页的页码
def get_max_page_num(bs):
    a_last_page = soup.find_all(name="a", text="尾页")
    last_page_num = a_last_page[0].get("href")
    last_page_num = re.search('index_(\d+)', last_page_num).group(1)
    last_page_num = int(last_page_num)
    return last_page_num


# 检查当前网址是否爬取过
def is_clawed(url, title):
    global STATIC_TABLE_NAME
    global STATIC_MYSQL_CUR

    # 先检查url地址是否被爬取
    url = str(url)
    sql = "select count(1) as c from " + STATIC_TABLE_NAME + " where url='%s'" % url
    STATIC_MYSQL_CUR.execute(sql)
    fetch = STATIC_MYSQL_CUR.fetchone()
    c = fetch[0]
    if c > 0:
        return True
    else:

        # 如果url地址没有被爬取，检查标题是否被爬取
        title = str(title)
        title = title.strip()
        sql = "select count(1) as c from " + STATIC_TABLE_NAME + " where title='%s'" % title
        STATIC_MYSQL_CUR.execute(sql)
        fetch = STATIC_MYSQL_CUR.fetchone()
        c = fetch[0]
        if c > 0:
            return True
        else:
            return False

        return False


# 插入爬取过的网址
def insert_clawed(url, title):
    url = str(url)
    global STATIC_TABLE_NAME
    global STATIC_MYSQL_CUR
    global STATIC_MYSQL_CON

    dateStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    sql = "insert into " + STATIC_TABLE_NAME + " (url,title,clawDate) values ('%s','%s','%s') " % (url, title, dateStr)
    STATIC_MYSQL_CUR.execute(sql)
    STATIC_MYSQL_CON.commit()


# 爬取当前页面并保存所有图片
def save_pics(a):
    global STATIC_PIC_SAVE_DIR
    global STATIC_HOST

    a_tile = str(a['title'])
    a_tile = a_tile.replace(":", "")
    folder_dir = STATIC_PIC_SAVE_DIR + a_tile
    folder_dir = folder_dir.replace("*", "")
    folder_dir = folder_dir.replace("?", "")
    folder_dir = folder_dir.replace("|", "")

    # 目录是否存在
    is_folder_exist = os.path.exists(folder_dir)
    # 如果不存在
    if not is_folder_exist:
        os.makedirs(folder_dir)
        print("目录%s创建成功" % folder_dir)

    a_href = a['href']
    a_html = get_html(STATIC_HOST + a_href)
    a_bs = BeautifulSoup(a_html, "lxml")

    td = a_bs.find_all(name="td", attrs={"class": "t_f"})
    if (len(td) == 0):
        return
    td = td[0]
    imgs = td.find_all("img")
    idx = 1
    for img in imgs:
        img_url = img['src']
        img_url = str(img_url)

        type_index = img_url.rfind(".")
        if type_index < 0:
            return

        img_type = img_url[img_url.rindex("."):]

        try:
            request.urlretrieve(img_url, folder_dir + "/%i%s" % (idx, img_type))
        except:
            time.sleep(2)
            try:
                request.urlretrieve(img_url, folder_dir + "/%i%s" % (idx, img_type))
            except:
                pass

        # request.urlretrieve(img_url, "d:/1.jpg")
        idx += 1
    print(imgs)


# 爬虫起始url
column_url = "http://www.yiren19.com/se/yazhousetu/"
column_html = get_html(column_url)
soup = BeautifulSoup(column_html, "lxml")

# 最大页码
max_page_num = get_max_page_num(bs=soup)

# 所有页码
page_urls = []
page_urls.append(column_url + "/index.html")
for i in range(2, max_page_num + 1):
    page_urls.append(column_url + "index_%i.html" % i)


# 爬取住方法
def star_claw():
    global ass
    exe_num = 0
    # 遍历a链接
    for a in ass:
        a_href = a['href']
        a_title = a['title']
        print('正在爬取%s' % str(a['title']))
        is_claw = is_clawed(a_href, a_title)
        if is_claw:
            print('已经爬取，跳过')
            pass
        else:
            save_pics(a)
            insert_clawed(a_href, str(a['title']))
        exe_num += 1
        print('已经爬取当前页面标题数%i,总个数%i' % (exe_num, len(ass)))


# 遍历所有页码
page_idx = 0
for page_url in page_urls:
    page_idx += 1
    ass = []

    # 获得当前页面的html
    page_html = get_html(page_url)

    if (page_html == None):
        continue

    # 转化为soup结构
    page_bs = BeautifulSoup(page_html, "lxml")

    # 找出当前页面的所有图片链接
    ul = page_bs.select('ul.textList')
    print(ul)
    ul0 = ul[0]
    print(ul0)

    # 所有指向图片的li链接
    a_s = ul0.find_all("a")

    # 获得符合条件的a链接
    for a in a_s:
        a_href = a['href']
        a_href = str(a_href)
        # a_href=""
        if ("yazhousetu" in a_href):
            ass.append(a)

    try:
        star_claw()

    except:
        print('链接异常，3秒后重试')
        time.sleep(3)
        star_claw()

    print('当前爬取页数：%i，总页数%i' % (page_idx, len(page_urls)))
