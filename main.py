import Dir
import MySql
import Process

# 生成一级文件夹
def get_dir():
    sort_lists = Process.classify()
    root = "网络小说/"
    if not Dir.check_dir("网络小说"):
        Dir.mkdir("网络小说")
    for dir_name in sort_lists.keys():
        if not Dir.check_dir(root + dir_name):
            Dir.mkdir(root + dir_name)


# 获取所有书籍的页面链接
def get_nuvel_url():
    sort_lists = Process.classify()
    Process.get_alllists(sort_lists)


# 获取所有书籍的页面数据
def get_novels_page(x):
    pass


if __name__ == '__main__':
    while True:
        print("--------------奇书网爬虫---------------------")
        print("请选择：")
        print("  1. 生成一级目录")
        print("  2. 抓取书籍链接")
        print("  3. 下载书籍")
        print("  4. 更新书籍")
        print("  0. 退出")
        print("  请输入：", end=" ")
        a = int(input())

        if a == 0:
            exit(0)
        elif a == 1:
            get_dir()
        elif a == 2:
            get_nuvel_url()
        elif a == 3:
            number = MySql.get_number()
            while True:
                x = int(input("请输入下载开始位置：（0≤x≤" + number))
                if x <=number or x >= 0:
                    break
            get_novels_page(x)
        elif a == 4:
            pass