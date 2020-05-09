import time

from lxml import etree
import Download
import MySql

def classify():
    print("正在获取分类信息")
    url = "http://wap.xqishuta.com/sort.html"

    response = Download.download_page(url, url)
    html = etree.HTML(response.content.decode("UTF-8"))
    url_lists = html.xpath("//div[@class='menu_nav']/ul/li/a/@href")
    name_list = html.xpath("//div[@class='menu_nav']/ul/li/a/text()")
    lists = {}
    for i in range(0, len(url_lists)):
        lists[name_list[i]] = "http://wap.xqishuta.com" + url_lists[i]
    print("分类信息：")
    for string in lists:
        print(string, end=" ")
    print("\n")
    return lists


def get_urllists(type, url):
    print("正在获取 {} 分类下书籍信息".format(type))
    first_url = url + "index_1.html"
    response = Download.download_page(first_url, url)
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
    print("{0} 分类下一共有 {1} 页数据".format(type, last_page))
    return url_list


def get_novellilsts(type, url):
    print("正在获取 {0} 分类下，{1} 页面数据".format(type, url))
    response = Download.download_page(url, url)
    html = etree.HTML(response.content.decode("UTF-8"))
    url_list = html.xpath("//div[@class='article']//h6/a/@href")
    novel_lists = []
    for string in url_list:
        temp = "http://wap.xqishuta.com/" + string[1:]
        novel_lists.append(temp)
    print("获取数据成功，该页面一共有 {} 本书籍".format(len(novel_lists)))
    return novel_lists


def get_alllists(classifylsts):
    for type in classifylsts.keys():
        urllists = get_urllists(type, classifylsts[type])
        for url in urllists:
            novellists = get_novellilsts(type, url)
            print("将 {0} 分类下 {1} 页面数据写入数据库".format(type, url))
            for url in novellists:
                MySql.insert_url(url)
            print("写入完成\n")
            time.sleep(1)

