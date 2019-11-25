from django.shortcuts import render
from .issue_form import FileForm, GitForm
from django.http.response import JsonResponse
from web.models import Issue, Project, Host, Host_Issue
from utils.pagination import Pagination
from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner, PlayBookRunner
from utils.git_helper import GitRepo
import time, os
from xitong.settings import git_path


def update(request):
    search = request.GET.get("table_search", "")
    # 根据项目名搜索
    updateall = Issue.objects.filter(project__name__contains=search)
    pages = Pagination(request.GET.get("page", 1), updateall.count(), request.GET.copy(), 10)
    return render(request, "file_update/updatelist.html",
                  {"page_title": "更新列表", "updateall": updateall[pages.start:pages.end],
                   "page_html": pages.page_html})


def handle_uploaded_file(files, t):
    '''
    上传文件方法
    :param files: 文件对象
    :param t:  时间戳（用来定义文件目录）
    :return:
    '''
    path = "/updata/file/{}".format(t)  # 通过时间戳 定义文件在服务器上的路径

    filename = [f.name for f in
                files]  # 将传来的files文件对象（列表） 通过循环取出文件名并存在filename列表中   f.name 取文件名(request.FILES获取到的数据的固定格式)

    # print(filename)    #打印filename列表（列表里全是本次上传的文件名）

    if "readme.xlsx" not in filename:  # 如果readme.xlsx文件名不存在于filename列表中（说明本次上传,没有上传readme.xlsx文件）     readme.xlsl文件（记录上传的文件、文件在项目中的位置）
        return False

    if not os.path.exists(path):  # 如果路径不存在，则创建路径
        os.makedirs(path)

    for f in files:  # 循环生成文件
        with open('{}/{}'.format(path, f.name), 'wb+') as destination:  # 部分是固定格式
            for chunk in f.chunks():
                destination.write(chunk)
    return True


def create_file(request):
    '''
    上传文件
    :param request:
    :return:
    '''
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)  # 固定格式
        t = int(time.time())  # 生成时间戳（用来生成文件路径）
        if form.is_valid():
            status = handle_uploaded_file(request.FILES.getlist('file_field'), t)  # 使用上传文件方法并传入 文件对象、时间戳 两个参数
            if not status:
                return JsonResponse({"status": 1, "msg": "请上传readme.xlsx文件"})
            form.instance.user = request.account  # 创建者字段
            form.instance.upload_path = t  # 上传文件路径字段
            form.instance.type = "0"  # 当前状态字段
            form.save()  # 保存在数据库中
            return JsonResponse({"status": 0, "msg": "操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request, "file_update/file_create.html", {"form": form})


####git更新：

#
def create_git(request):
    '''
    更新指定项目的git目录
    :param request:
    :return:
    '''

    form = GitForm()
    if request.method == "POST":
        form = GitForm(request.POST)
        print(request.POST)
        t = int(time.time())
        if form.is_valid():
            print(form.cleaned_data)
            form.instance.user = request.account
            form.instance.upload_path = t
            form.instance.type = "1"  # 更新类型  1：git更新

            # 项目目录  （要被更新的目录）
            path = git_path+form.cleaned_data["project"].name

            # 执行 指定项目git目录的更新
            # 如果是分支更新
            if request.POST.get("type") == "bra":
                print("分支更新")
                # 传入项目目录，执行checkout方法（传入分支名和 commit哈希）
                GitRepo(path).checkout(request.POST.get("bra_name"), request.POST.get("com_name"))
            # 否则（通过tag更新）：
            else:
                GitRepo(path).checkout(request.POST.get("tag_name"), type="tag")
            #form.save() 将数据保存到更新表中,   issue=form.save() 获取本次更新对象
            print("开始保存")
            issue=form.save()
            #Host_Issue表保存issue字段、host字段
                #循环项目中的主机对象
            for i in form.cleaned_data["project"].server_host.all():
                #新增保存issue字段、host字段
                Host_Issue.objects.create(issue=issue,host=i)
            return JsonResponse({"status": 0, "msg": "操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request, "file_update/git_create.html", {"form": form})


def get_branch(request, pk):
    '''
    通过获取到的pk，查找项目，获取项目的分支
    :param request:
    :param pk:   项目id
    :return:
    '''
    # 查询项目对象
    project = Project.objects.filter(pk=pk).first()
    # 获取项目地址
    path = git_path+project.name
    # 传入项目地址,执行get_branch方法   res=获取分支信息
    res = GitRepo(path).get_branch()
    # 返回给前端页面分支信息
    return JsonResponse({"branch": res})


def get_commit(request, pk, bra):
    '''
    获取commit提交信息
    :param request:
    :param pk:  项目id
    :param bra: 分支信息
    :return:
    '''
    # 获取项目对象
    project = Project.objects.filter(pk=pk).first()
    # 获取项目地址
    path = git_path+project.name
    # 传入项目地址, 执行get_commit方法  传入分支信息，   res=获取commit信息
    res = GitRepo(path).get_commit(bra)
    print("ressss", res)
    # 将commit信息传给前端
    return JsonResponse({"commits": res})


def get_tag(request, pk):
    '''
    获取tag信息
    :param request:
    :param pk:
    :return:
    '''
    project = Project.objects.filter(pk=pk).first()
    path = git_path+project.name
    res = GitRepo(path).get_tag()
    return JsonResponse({"tag": res})


#####发布、更新项目

from .issue_form import Upload_one


def upload_one(request,pk):
    '''
    找到要更新的项目
    在项目中找一台主机
    下线主机 备份代码  更新项目（复制代码到下线主机项目目录下，覆盖原来的代码）
    运行测试
    成功后上线主机、不成功则根据之前备份的代码恢复项目
    :param request:
    :param pk:  更新表数据的id
    :return:
    '''

    # 获取项目
    # 先根据id获取更新对象(传给前端循环对象取值，所以不加first)
    issue = Issue.objects.filter(pk=pk)
    # 先根据id获取更新对象
    issue_first = Issue.objects.filter(pk=pk).first()
    # 根据更新对象获取更新的项目对象
    project = issue_first.project
    # 根据项目对象获取主机对象
    host_list = project.server_host.all()
    # 设置多选，传入主机对象
    form = Upload_one(host_list)
    # 如果提交（执行更新操作）   此时用户已经完成选择主机（需要被更新项目的后端主机）的操作
    # 用户提交后,通过request.POST可以获得更新类型（灰度发布、多选发布）、后端主机
    # request.post获取（灰度发布）：'type': ['hd'], 'hd_name': ['192.168.179.142']
    # request.post获取（多选发布）'type': ['dx'], 'hd_name': ['0'], 'server_host': ['7']  :
    if request.method == "POST":
        print("数据", request.POST)
        print("提交操作")
        # 更新状态字段变为更新中
        issue_first.status = "1"
        # 保存
        issue_first.save()
        #灰度发布（先发布一台）
        if request.POST["type"] == "hd":
            # 后端主机ip：
            print("发布类型灰度！")
            server_ip = request.POST["hd_name"]
            if server_ip=="0":
                return JsonResponse({"status": 1})
            # 后端主机对象
            hd_host = Host.objects.filter(hostip=request.POST["hd_name"])
            # # 执行nginx方法(下线主机)
            # nginx_status = nginx(project.nginx_host.all(), project.nginx_conf, server_ip, "out")
            # 执行server_push方法(备份远程主机代码,复制本地项目代码到远程主机项目中)
            push_status = server_push(project.path, project.name, issue_first.upload_path, issue_first.type, hd_host)
            #如果nginx方法和server_push方法都执行成功
            if  push_status:
                # 更新状态字段变为等待测试
                issue_first.status = "2"
                issue_first.save()
                return JsonResponse({"status":0,"msg":"更新成功!"})
            else:
                # 更新状态字段变为更新失败
                issue_first.status = "5"
                issue_first.save()
                return JsonResponse({"status": 1, "msg": "更新失败!"})

    return render(request, "file_update/upload_one.html", {"issue": issue, "hosts": host_list, "form": form})


def nginx(nginx_host, nginx_conf, server_ip, type):
    '''
    根据nginx 让后端主机下线、上线
    :param nginx_host: 此项目的nginx主机
    :param nginx_conf: 此项目nginx 主机的配置文件
    :param server_ip: 后端主机Ip
    :param type: up(上线)、out(下线)
    :return:
    '''
    if type == "out":
        # 下线(nginx配置文件里注释后端主机ip)：
        # 使用replace 替换模块：
        # 参数：path 被替换文件路径    regexp 匹配字符   replace 替换字符  \转义
        task = [{"action": {"module": "replace",
                            "args": "path={} regexp=(.*{}.*) replace=#\\1".format(nginx_conf, server_ip)}}]
    else:
        # 上线,nginx配置文件取消注释
        task = [{"action": {"module": "replace",
                            "args": "path={} regexp=#(.*{}.*) replace=\\1".format(nginx_conf, server_ip)}}]
    # 重启nginx：
    task.append({"action": {"module": "service", "args": "name=nginx state=reloaded"}})

    status = ansible_helper(nginx_host, task)
    return True if status else False


# 导入openpyxl 读取xlsx文件
from  openpyxl import load_workbook
# 导入本地项目路径
from  xitong.settings import git_path,server_backup_path


def server_push(project_path, project_name, t, update_type, server_host):
    '''
    备份后端主机项目代码  放在后端主机的备份目录里
    将代码复制到后端主机项目目录中

    :param project_path:远程项目路径
    :param project_name:项目名（定义备份路径）
    :param t:时间戳（定义备份路径）
    :param update_type:更新类型
    :param server_host:后端主机
    :return:
    '''
    # 备份：
    task = [{"action": {"module": "shell",
                        "args": "tar zcf {}/{}/{}.tar.gz {}".format(server_backup_path,project_name,t,project_path)}}]
    # 将代码复制到远程主机项目目录中：
    # git更新
    if update_type == "1":

        # 注意 copy模块  src（源）不加/ 代表复制目录， 最后有/ 代表复制目录下所有文件
        task.append(
            {"action": {"module": "copy", "args": "src={}/ dest={}".format(git_path + project_name, project_path)}})

    else:
        print("文件更新!")
        # 文件更新:
        # 文件上传后存放目录
        path = "/updata/file/{}".format(t)
        # 生成读readme.xlsx对象       每行：1.文件名 2.将要传到项目的路径
        wb = load_workbook("{}/readme.xlsx".format(path))
        # 获取第一个工作簿对象
        wb1 = wb.active
        # 循环工作簿行
        for r in wb1.rows:
            # 从readme.xlsx 读每行第一个（文件名），第二个（要放在项目哪个路径下）,制作ansible命令
            #可以使用copy模块 也可以使用synchronize模块（可能会快一点），除模块名其他地方不用修改
            task.append({"action": {"module": "copy",
                                    "args": "src={}/{} dest={}{}".format(path, r[0].value, project_path, r[1].value)}})
    print("开始copy")
    status = ansible_helper(server_host, task)
    print("copy结束！")
    return True if status else False


def ansible_helper(host_list, task):
    '''
    远程执行任务
    :param host_list:  主机对象
    :param task: 具体任务
    :return:
    '''
    host_data = [{"hostname": h.name, "ip": h.hostip, "port": h.ssh_port, } for h in host_list]  # 主机列表
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    ret = runner.run(task)
    # ret.results_raw 返回结果（字典），如果有["ok"]这个key说明执行成功返回True，否则返回false
    return True if ret.results_raw["ok"] else False
