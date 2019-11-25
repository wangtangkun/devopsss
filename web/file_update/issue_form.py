from web.models import Issue,Project
from utils.auth import NewModelForm
from django.core.exceptions import ValidationError
from django import forms


class FileForm(NewModelForm):
    #固定格式（一次性可以上传多个文件），label自定义
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),label="上传文件")

    class Meta:
        model=Issue
        fields=["project","file_field"]   #页面上只显示 项目名、上传文件框


class GitForm(NewModelForm):

    class Meta:
        model=Issue
        fields=["project","backup"]

class Upload_one(NewModelForm):

    def __init__(self,host_list,*args,**kwargs):
        super(Upload_one,self).__init__(*args,**kwargs)
        #通过传入的host_list对象列表，定义server_host字段选项
        self.fields["server_host"].choices=[(du.pk,du.hostip) for du in host_list]
    class Meta:
        model=Project
        fields=["server_host"]

