#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.conf.urls import url
from web.user.user import *

from web.host.host import *
from web.init.init import *
from web.views import *
from web.project.project import *
from web.command.command import *
from web.cron.cron import  *

from web.file_update.issue import *
urlpatterns = [
    url(r'^index/',index,name="index"),
    url(r'^login/',login,name="login"),
    #url(r'^create_host/',create_host,name="create_host"),
    #用户信息
    url(r'^userlist/',userlist,name="userlist"),
    url(r'^create_user/',create_edit_user,name="create_user"),
    url(r'^edit_user/(\d+)$',create_edit_user,name="edit_user"),
    url(r'^del_user/(\d+)$',del_user,name="del_user"),
    #主机信息
    url(r'^hostlist/',Hostlist,name="hostlist"),
    url(r'^create_host/',Create_edit_host,name="create_host"),
    url(r'^edit_host/(\d+)$',Create_edit_host,name="edit_host"),
    url(r'^del_host/(\d+)$',del_host,name="del_host"),
    # init信息
    url(r'^initlist/$', initlist, name="initlist"),
    url(r'^createinit/$', create_init, name="create_init"),
    url(r'^editinit/(\d+)$', create_init, name="edit_init"),
    url(r'^delinit/(\d+)$', del_init, name="del_init"),
    # init log
    url(r'^createlog/$', create_initlog, name="create_log"),
    url(r'^logslist/(\d+)$', initlog, name="logslist"),

    #项目信息
    url(r'^projectlist/',Projectlist,name="project_list"),
    url(r'^create_project/',Create_edit_project,name="create_project"),
    url(r'^edit_project/(\d+)$',Create_edit_project,name="edit_project"),
    url(r'^del_project/(\d+)$',del_project,name="del_project"),

    #命令下发,展示,详情
    url(r'^command_list/$', command_list, name="command_list"),
    url(r'^command_issued/',command_issued,name="command_issued"),
    url(r'^command_details/(\d+)$',command_details,name="command_details"),

    # #定时任务
    url(r'^create_cron/', Create_edit_cron, name="create_cron"),
    url(r'^edit_cron/(\d+)$', Create_edit_cron, name="edit_cron"),
    url(r'^cron_list/$', cron_list, name="cron_list"),
    url(r'^delcron/(\d+)$', del_cron, name="del_cron"),
    url(r'^delcron/(\d+)$', del_cron, name="del_cron"),

#更新相关
    #展示更新页面
    url(r'^update/$', update, name="update"),
    #展示回滚页面
    url(r'^gobackall/$', gobackall, name="gobackall"),
    #上传文件页面
    url(r'^file/$', create_file, name="create_file"),


    #更新git页面
    url(r'^git/$', create_git, name="create_git"),
        #获取分支信息（显示在更新git页面）
    url(r'get_branch/(\d+)$',get_branch),
        #获取tag信息（显示在更新git页面）
    url(r'get_tag/(\d+)$',get_tag),
        #获取commit信息（显示在更新git页面）
    url(r'get_commit/(\d+)/(\w+)$',get_commit),

#发布、更新项目
    #发布或更新一台主机（灰度发布特性先更新一台主机（下线主机-更新代码-测试））
    url(r"upload_one/(\d+)$",upload_one,name="upload_one"),

    #测试通过,上线主机
    url(r"sucessfully/(\d+)$",sucessfully,name="sucessfully"),
    #详情页
    url(r"issue_detail/(\d+)$",issue_detail,name="issue_detail"),

    #更新剩余主机
    url(r"update_again/(\d+)$",update_again,name="update_again"),
    #测试通过主机 上线剩余主机
    url(r"success_again/(\d+)$",success_again,name="success_again"),
    #回滚
    url(r"go_back/(\d+)$",go_back,name="go_back"),
]
