from django.shortcuts import render
from .issue_form import FileForm,GitForm
from django.http.response import JsonResponse
from web.models import Issue,Project
from utils.pagination import Pagination
from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner,PlayBookRunner
from utils.git_helper import GitRepo

import time,os

def update(request):
    search=request.GET.get("table_search","")
    #根据项目名搜索
    updateall=Issue.objects.filter(project__name__contains=search)
    pages=Pagination(request.GET.get("page",1),updateall.count(),request.GET.copy(),10)
    return render(request,"file_update/updatelist.html",{"page_title":"更新列表","updateall":updateall[pages.start:pages.end],
                                           "page_html":pages.page_html})


def handle_uploaded_file(files,t):
    '''
    上传文件方法
    :param files: 文件对象
    :param t:  时间戳（用来定义文件目录）
    :return:
    '''
    path="/updata/file/{}".format(t)   #通过时间戳 定义文件在服务器上的路径

    filename=[f.name for f in files]  #将传来的files文件对象（列表） 通过循环取出文件名并存在filename列表中   f.name 取文件名(request.FILES获取到的数据的固定格式)

    #print(filename)    #打印filename列表（列表里全是本次上传的文件名）

    if "readme.xlsx" not in filename:  #如果readme.xlsx文件名不存在于filename列表中（说明本次上传,没有上传readme.xlsx文件）     readme.xlsl文件（记录上传的文件、文件在项目中的位置）
        return False

    if not os.path.exists(path):   #如果路径不存在，则创建路径
        os.makedirs(path)

    for f in files:   #循环生成文件
        with open('{}/{}'.format(path,f.name), 'wb+') as destination: #部分是固定格式
            for chunk in f.chunks():
                destination.write(chunk)
    return True

def create_file(request):
    '''
    上传文件
    :param request:
    :return:
    '''
    form=FileForm()
    if request.method=="POST":
        form=FileForm(request.POST, request.FILES)  #固定格式
        t=int(time.time())   #生成时间戳（用来生成文件路径）
        if form.is_valid():
            status=handle_uploaded_file(request.FILES.getlist('file_field'),t)  #使用上传文件方法并传入 文件对象、时间戳 两个参数
            if not status:
                return JsonResponse({"status":1,"msg":"请上传readme.xlsx文件"})
            form.instance.user=request.account  #创建者字段
            form.instance.upload_path=t         #上传文件路径字段
            form.instance.type="0"              #当前状态字段
            form.save()                         #保存在数据库中
            return JsonResponse({"status":0,"msg":"操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request,"file_update/file_create.html",{"form":form})




####git更新：

#
def create_git(request):
    '''
    更新git
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
            form.instance.type = "1"   #更新类型  1：git更新
            path="/updata/git/{}".format(form.cleaned_data["project"].name)
            if request.POST.get("type") =="bra":
                GitRepo(path).checkout(request.POST.get("bra_name"),request.POST.get("com_name"))
            else:
                GitRepo(path).checkout(request.POST.get("tag_name"),type="tag")
            form.save()
            return JsonResponse({"status": 0, "msg": "操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request, "file_update/git_create.html", {"form": form})


def get_branch(request,pk):
    '''
    通过获取到的pk，查找项目，获取项目的分支
    :param request:
    :param pk:   项目id
    :return:
    '''
    #查询项目对象
    project=Project.objects.filter(pk=pk).first()
    #获取项目地址
    path=project.path
    #传入项目地址,执行get_branch方法   res=获取分支信息
    res=GitRepo(path).get_branch()

    #返回给前端页面分支信息
    return JsonResponse({"branch":res})


def get_commit(request,pk,bra):
    '''
    获取commit提交信息
    :param request:
    :param pk:  项目id
    :param bra: 分支信息
    :return:
    '''
    #获取项目对象
    project = Project.objects.filter(pk=pk).first()
    # 获取项目地址
    path = project.path
    #传入项目地址, 执行get_commit方法  传入分支信息，   res=获取commit信息
    res = GitRepo(path).get_commit(bra)

    #将commit信息传给前端
    return JsonResponse({"commits": res})


def get_tag(request,pk):
    '''
    获取tag信息
    :param request:
    :param pk:
    :return:
    '''
    project=Project.objects.filter(pk=pk).first()
    path=project.path
    res=GitRepo(path).get_tag()
    return JsonResponse({"tag":res})


