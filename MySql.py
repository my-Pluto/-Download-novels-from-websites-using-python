import time

import pymysql

sqlname = "root"
password = "qdlgdx"
table = "novels"
host = "localhost"


def insert_url(url):
    db = pymysql.connect(host, sqlname, password, table)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = """INSERT INTO novels(link, ys)
             VALUES ('{}', 'no')""".format(url)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def update(novel):
    db = pymysql.connect(host, sqlname, password, table)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    type = novel['type']
    name = novel['name']
    link = novel['link']
    date = novel['date']
    img = novel['img']
    text_link = novel['text_link']
    ys = 'no'

    date = time.strptime(date, "%Y-%m-%d")
    # SQL 插入语句
    sql = "UPDATE novels SET type='" + type + "', name='" + name + "', date='" + time.strftime("%Y-%m-%d",
                                                                                               date) + "', ys='" + ys \
          + "', img='" + img + "', text_link='" + text_link + "' WHERE link='" + link + "'"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def select(url):
    # 打开数据库连接
    db = pymysql.connect(host, sqlname, password, table)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM novels WHERE link='" + url + "'"
    rs = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            novel = {'ytpe': row[0], 'name': row[1], 'link': row[2], 'date': row[3], 'ys': row[4]}
            rs.append(novel)

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return rs


def select_all(x):
    db = pymysql.connect(host, sqlname, password, table)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT link FROM novels limit " + str(x) + ", 100"
    rs = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        for row in results:
            rs.append(row[0])
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return rs


def get_number():
    db = pymysql.connect(host, sqlname, password, table)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT COUNT(*) FROM novels"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        for row in results:
            number = row[0]
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return number
