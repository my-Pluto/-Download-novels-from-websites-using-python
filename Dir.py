"""
    该文件用于检测目录是否存在以及创建目录
"""

import os

# 检测文件夹是否存在
def check_dir(path):
    return os.path.exists(path)


# 创建文件夹
def mkdir(path):
    os.makedirs(path)
