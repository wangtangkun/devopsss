#！/usr/bin/env python
#-*- coding:utf-8 -*-

from utils.ansible2.runner import AdHocRunner, CommandRunner, PlayBookRunner
from utils.ansible2.inventory import Inventory

def Remote_directory(host_list,backup_path,path):
    '''
    在远程主机上创建备份目录 和项目目录
    :param backup_path: 备份目录
    :param path: 项目目录
    :return:
    '''
    host_data = [
        {
            "hostname": h.name,
            "ip": h.hostip,
        } for h in host_list
    ]
    inventory = Inventory(host_data)  # 重新组成虚拟组
    runner = CommandRunner(inventory)
    #创建备份目录 creates 检测目录是否存在,存在则不执行后面的mkdir
    res = runner.execute('creates={} mkdir {} -p'.format(backup_path,backup_path))
    #创建项目目录
    ret = runner.execute('creates={} mkdir {} -p'.format(path,path))

    return True if res.results_raw["ok"] and  ret.results_raw["ok"] else False