import time

from lxml import etree

import Dir
import Download
import MySql
from Logger import Logger

error_url = []

root = "网络小说"


def prints(string, *args):
    Logger().write(string + "\n")


# 获取网站分类信息
def classify():
    prints("正在获取分类信息")
    url = "http://wap.xqishuta.com/sort.html"

    for i in range(1, 4):
        try:
            response = Download.download_page(url, url)
            break
        except:
            if i != 3:
                prints("第 {0} 次获取 {1} 页面信息失败".format(i, url))
                continue
            else:
                prints("获取 {} 页面信息失败，退出程序".format(url))
                exit(0)
    html = etree.HTML(response.content.decode("UTF-8"))
    url_lists = html.xpath("//div[@class='menu_nav']/ul/li/a/@href")
    name_list = html.xpath("//div[@class='menu_nav']/ul/li/a/text()")
    lists = {}
    for i in range(0, len(url_lists)):
        lists[name_list[i]] = "http://wap.xqishuta.com" + url_lists[i]
    prints("分类信息：")
    for string in lists:
        prints(string, " ")
    prints("\n")
    return lists


# 获取页面下书籍总页数
def get_urllists(type, url):
    prints("正在获取 {} 分类下书籍信息".format(type))
    first_url = url + "index_1.html"

    for i in range(1, 4):
        try:
            response = Download.download_page(first_url, url)
            break
        except:
            if i != 3:
                prints("第 {0} 次获取 {1} 页面信息失败".format(i, url))
                continue
            else:
                prints("获取 {} 页面信息失败".format(url))
                error_url.append(first_url)
                return

    html = etree.HTML(response.content.decode("UTF-8"))
    temp = html.xpath("//div[@class='page']/a/@href")
    temp = temp[1]
    temp = temp.split(".")
    temp = temp[0].split("_")
    last_page = int(str(temp[1]))
    url_list = []
    for i in range(1, last_page + 1):
        temp = url + "index_" + str(i) + ".html"
        url_list.append(temp)
    prints("{0} 分类下一共有 {1} 页数据".format(type, last_page))
    return url_list


# 获取每一页上的书籍链接
def get_novellilsts(type, url):
    prints("-----------------------------------------------------")
    prints("正在获取 {0} 分类下，{1} 页面数据".format(type, url))

    for i in range(1, 4):
        try:
            response = Download.download_page(url, url)
            break
        except:
            if i != 3:
                prints("第 {0} 次获取 {1} 页面信息失败".format(i, url))
                continue
            else:
                prints("获取 {} 页面信息失败".format(url))
                error_url.append(url)
                return

    html = etree.HTML(response.content.decode("UTF-8"))
    url_list = html.xpath("//div[@class='article']//h6/a/@href")
    novel_lists = []
    for string in url_list:
        temp = "http://wap.xqishuta.com/" + string[1:]
        novel_lists.append(temp)
    prints("获取数据成功，该页面一共有 {} 本书籍".format(len(novel_lists)))
    return novel_lists


# 获取整个网站的书籍链接并写入数据库
def get_alllists(classifylsts):
    for type in classifylsts.keys():
        urllists = get_urllists(type, classifylsts[type])
        for url in urllists:
            novellists = get_novellilsts(type, url)
            prints("将 {0} 分类下 {1} 页面数据写入数据库".format(type, url))
            for url in novellists:
                MySql.insert_url(url)
            prints("写入完成\n")
            time.sleep(1)


def get_novel(url):
    prints("------------------------------------------------------")
    prints("正在下载 {0} 页面小说".format(url))

    for i in range(1, 4):
        try:
            response = Download.download_page(url, url)
            break
        except:
            if i != 3:
                prints("第 {0} 次获取 {1} 页面信息失败".format(i, url))
                continue
            else:
                prints("获取 {} 页面信息失败".format(url))
                error_url.append(url)
                return

    html = etree.HTML(response.content.decode("UTF-8"))

    img = html.xpath("//div[@class='pic']/img/@src")[0]
    name = html.xpath("//div[@class='cataloginfo']/h3/text()")[0]

    temp = html.xpath("//div[@class='infotype']/p/text()")
    author = temp[0].split("：")[1]
    type = temp[1].split("：")[1]
    date = temp[2].split("：")[1].split("T")[0]

    link = html.xpath("//ul[@class='infolink']//p/script/text()")[0].split("'")[3]

    information = html.xpath("//div[@class='intro']/p/text()")[0]

    prints("图片地址：" + img)
    prints("书籍名称：" + name)
    prints("作者：" + author)
    prints("类型:" + type)
    prints("最后更新时间：" + date)
    prints("下载地址：" + link)
    prints("小说简介：" + information)

    novel = {
        "link": url,
        "img": img,
        "author": author,
        "name": name,
        "type": type,
        "date": date,
        "text_link": link,
        "小说简介": information
    }
    return novel


def get_all_novels_page(x):
    number = MySql.get_number() - x
    while True:
        i = 1
        urls = MySql.select_all(x)
        for url in urls:
            flag = False
            prints("正在下载第 {} 本书籍数据".format(x + i))
            novel = get_novel(url)
            path = root + "/" + novel['type'] + "/" + novel['name']
            if not Dir.check_dir(path):
                Dir.mkdir(path)
            prints("开始下载书籍txt")
            for i in range(1, 4):
                try:
                    Download.download_text(novel['text_link'], path + "/")
                    break
                except:
                    if i != 3:
                        prints("第 {0} 次下载小说 《{1}》 失败".format(i, novel['name']))
                        continue
                    else:
                        prints("获取 {} 小说失败".format(novel['name']))
                        error_url.append(novel['link'])
                        flag = True
                        break
            prints("书籍下载完成，开始下载封面")
            for i in range(1, 4):
                try:
                    Download.download_text(novel['img'], path)
                    break
                except:
                    if i != 3:
                        prints("第 {0} 次下载小说 《{1}》 封面失败".format(i, novel['name']))
                        continue
                    else:
                        prints("获取 {} 小说封面失败".format(novel['name']))
                        error_url.append(novel['link'])
                        flag = True
                        break

            if flag is True:
                continue
            flag = False

            string = "小说名称：" + novel['name'] + "\n作    者：" + novel['author'] + "\n类    型:" + novel['type'] + \
                     "\n最后更新时间：" + novel['date'] + "\n下载地址：" + novel['link'] + "\n图片地址：" + novel['img'] + \
                     "\n小说简介：" + novel['小说简介']

            with open(path + "/图书信息.txt", 'w', encoding="UTF-8") as f:
                f.write(string + "\n")
                f.close()

            MySql.update(novel)
            i = i + 1
            if i == 20:
                time.sleep(2)
        if x + 100 <= number:
            x = x + 100
        else:
            break
    prints("所有书籍数据采集完成！")


if __name__ == '__main__':
    get_all_novels_page(0)
