# coding:utf-8

import os
import sys

try:
    import configparser
except Exception as e:
    print("module is't installed,please used 'pip install configparser' commmond to install it")


# 返回当前脚本的全路径，末尾不带\
def getthispath():
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.split(path)[0]


def get_file_ext(path):
    print(os.path.splitext(path))
    # return os.path.splitext(path)[1]


# 获取路径的父目录，末尾不带\
def getparent(filepath):
    if not filepath:
        return None
    lsPath = os.path.split(filepath)
    # print(lsPath)
    # print("lsPath[1] = %s" %lsPath[1])
    if lsPath[1]:
        return lsPath[0]
    lsPath = os.path.split(lsPath[0])
    return lsPath[0]


# 创建多级目录，比如c:\\test1\\test2,如果test1 test2都不存在，都将被创建
def create_dirs(to_create_path):
    path_create = to_create_path
    if os.sep == '\\':
        path_create = path_create.replace('/', os.sep)
    dirs = path_create.split(os.sep)
    path = ''
    for dir in dirs:
        dir += os.sep
        path = os.path.join(path, dir)
        if not os.path.exists(path):
            os.mkdir(path, 0o777)

    if not os.path.exists(to_create_path):
        return False
    return True


def delete_file(to_del_file):
    if os.path.exists(to_del_file):
        os.remove(to_del_file)

    if not os.path.exists(to_del_file):
        return True
    else:
        return False

