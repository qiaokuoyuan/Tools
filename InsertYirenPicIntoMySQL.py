# 本文件用于将已经保存的艺人图片转化到mysql记录中，防止重复爬取；
# 由于mysql数据库内容丢失，而保存的文件还在，所以根据已经保存的文件信息，恢复mysql记录，但是这种方式恢复的记录中url信息字段丢失

import pymysql
import time

STATIC_DB_NAME = "yiren"
STATIC_TABLE_NAME = "yiren_pic"
STATIC_PIC_SAVE_DIR = 'd:/d/yiren_pic/'

STATIC_HOST = 'http://www.yiren19.com'
STATIC_MYSQL_CON = pymysql.connect(host="127.0.0.1", user="root", password="root", db=STATIC_DB_NAME, charset="utf8")
STATIC_MYSQL_CUR = STATIC_MYSQL_CON.cursor()

ass = []


# 读取爬取过的文件的文件夹，插入mysql
def insertMySQLFromClawedPicFolder():
    import os

    global STATIC_MYSQL_CUR
    global STATIC_MYSQL_CON

    folders = os.listdir(STATIC_PIC_SAVE_DIR)
    for folder in folders:
        folder_name = str(folder)
        folder_name = folder_name.strip()

        dateStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql = "insert into " + STATIC_TABLE_NAME + " (url,title,clawDate) values ('%s','%s','%s') " % (
            "从folder中补", folder_name, dateStr)

        print(sql)
        STATIC_MYSQL_CUR.execute(sql)
        STATIC_MYSQL_CON.commit()
    print('finished')
    pass


insertMySQLFromClawedPicFolder()
