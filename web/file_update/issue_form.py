from web.models import Issue
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

