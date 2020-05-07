from lxml import etree
from Download import Download


class Process():
    @staticmethod
    def classify():
        url = "http://wap.xqishuta.com/sort.html"

        response = Download.download_page(url, url)
        html = etree.HTML(response.content.decode("UTF-8"))
        url_lists = html.xpath("//div[@class='menu_nav']/ul/li/a/@href")
        name_list = html.xpath("//div[@class='menu_nav']/ul/li/a/text()")
        lists = {}
        for i in range(0, len(url_lists)):
            lists[name_list[i]] = "http://wap.xqishuta.com" + url_lists[i]

        return lists