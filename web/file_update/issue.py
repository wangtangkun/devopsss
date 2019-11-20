from django.shortcuts import render
from .issue_form import FileForm
from django.http.response import JsonResponse
from web.models import Issue
from utils.pagination import Pagination


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







## 初始化
## 初始化日志 ansible api 去执行playbook


# 实现项目的增删该查


