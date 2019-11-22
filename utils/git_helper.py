


import os,sys


from git import Repo
from git import Git
import git
import subprocess
class GitRepo():

    def __init__(self,path):
        self.path=path




    def is_dir(self,url):
        '''
        检测路径，不符合则从远程克隆到服务器里
        :param url: 传来的远程git地址
        :return:
        '''
        #定义path，  由传来的path和.git组合：path/.git    .git可以判断当前目录是否是一个git目录
        path=os.path.join(self.path,".git")

        #如果路径不存在
        if not os.path.exists(path):
            print("开始克隆")
            print("url",url)

            #从远程仓库克隆到self.path路径下   self.path(纯路径，不含.git文件)
            Repo.clone_from(url,self.path)


    def get_branch(self):
        '''
        获取分支信息
        :return:
        '''

        #定义repo对象
        repo=Repo(self.path)
        #同步远程仓库分支到本地git目录
        Git(self.path).fetch()

        #注意：
        #远程仓库可以创建分支
        #linux服务器 项目目录下也可以创建分支
        # 下面获取到的这些分支 与linux项目上创建的分支没有关系，是从远程仓库中获取的。
        #获取分支方法：
                #1.linux项目目录中创建分支,推送到远程仓库
                #2.远程仓库创建分支
                #3.克隆远程仓库项目到linux服务器中



        # for b in repo.remote().refs:
        #     print(b)
        # 打印结果(根据上面从远程仓库克隆项目，实际远程的分支也都克隆下来了，但使用repo.remote().branchs只能获取到master,要用到repo.remote().refs才能显示齐全), 如果之后 1. linux项目目录中创建分支,推送到远程仓库、2.远程仓库创建分支    都可以显示出来：
            # origin / HEAD
            # origin / dev
            # origin / master
            # origin / nimei
            # origin / test
            # origin / testtt


        #返回分支信息,过滤并选择 部分信息返回
        return [str(b).split("/")[1] for b in repo.remote().refs if str(b) !="origin/HEAD"]


    def get_commit(self,bra):
        '''
        获取commit信息
        :param bra:  分支信息
        :return:
        '''

        # 将本地的分支强制与origin/分支一致,回到到远程仓库最新状态
        try:
            active = Repo(self.path).active_branch
        except Exception as e:
            active = "master"
        subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path, active))
        Git(self.path).checkout(bra)# 因为本地没有这个分支，所以才会报错，先切换这个分支，还能下载
        return [{"id":commit.hexsha,"msg":commit.message} for commit in Repo(self.path).iter_commits(bra)]
    #

    def get_tag(self):
        '''
        获取tag信息
        :return:
        '''
        return [str(t) for t in Repo(self.path).tags]


    # def checkout(self,msg,commit=None,type=None):
    #     #查看当前所在分支
    #     try:
    #         active=Repo(self.path).active_branch
    #     #捕获所有异常：
    #     #定义active="master"
    #     except Exception as e:
    #         active="master"
    #     #进入git目录,并回退到远程仓库
    #     subprocess.getoutput("cd {} && git reset --hard origin/{}".format(self.path,active))
    #     Git(self.path).checkout(msg)
    #     if type !=None:
    #         Repo(self.path).index.reset(commit=commit,head=True)

### 实现
# 发布
# 灰度发布
# 先发布一台
# 测试
#发布剩余的
# 回滚 cp