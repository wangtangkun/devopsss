from git import Repo
from git import Git

####通过python操作 git


#本地的git目录
#repo=Repo(r"G:\test\untitled\xitong")

# git add .
# repo.index.add(["a.txt"])  #将a.txt文件放入缓存区，相当于git add .  只要运行当前py即可 以下不再描述


# git commit -m
# repo.index.commit("这是gitpython提交的数据")


#git reset --hard hash值   #将本地仓库 回退到工作区
#repo.index.reset(commit="54c89f56200d30e8421158ab62b52957b1e7452e", head=True)   #commit 相当于 hash值


 
# git branch     #查看分支
#print([str(r) for r in repo.branches])


# git clone https://url.git    #克隆项目
# repo.clone_from()


# git remote add origin https://url.git   #建立远程仓库连接关系
# repo.create_remote("test",)


# git branch name    #创建分支
#repo.create_head("test")  #test 分支名


# git tag -a name -m ""   #创建标签
#repo.create_tag("v2.0")


# git tag    #查看标签
# print(repo.tags)



# print(repo.active_branch)     #查看当前所在分支



# git branch -d name    #删除分支
# repo.delete_head()



# git tag -d name     #删除标签
# repo.delete_tag()



# 获取分支的提交记录
# for c in repo.iter_commits("dev"):     #dev 指定查看的分支
    # 获取提交的message（commit -m "" 提交时写的东西）
    #print(c.message)
    # 获取提交的hash值
    # print(c.hexsha)




#git pull origin dev   #拉取     #dev 拉取远程的dev分支
# repo.remote().pull("dev")

#git push origin dev   #推送     #推送到远程的 dev分支
# repo.remote().push("dev")


#####另一种方法, Git模块:

#本地git目录
# r=Git("D:\新电脑\zdh")

#将文件加入缓存区
# r.add("c.py")

#提交文件到本地仓库
# r.commit("-m 新增c.py")

#切换分支
# r.checkout("master")

#查看当前分支
# repo=Repo("D:\新电脑\zdh")
# print(repo.active_branch)



