from Dir import Dir
from Process import Process

if __name__ == '__main__':
    sort_lists = Process.classify()
    for dir_name in sort_lists.keys():
        if not Dir.check_dir(dir_name):
            Dir.mkdir(dir_name)