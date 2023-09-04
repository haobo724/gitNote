# Git的基本工作流程
===默认远程仓库名为origin===
1. 从**Remote** repository `clone`项目到本地repository
2. 在本地repository中新建一个branch用于对项目的修改 `git checkout -b my-feature` (不仅仅是新建了branch而且隐式的把当前的branch内容也复制过去)
   1. 特别注意：如果要工作的分支不是主分支，而是功能分支，而且本地之前没有这个分支，那clone之后要在本地新建，并且在pull一次
   2. 如果不确定本地和远程哪个版本更新，可以使用 `git log -1` 查看当前commit版本，然后对比
3. 进行代码开发
    + 开发完成后，建议使用`git diff` 查看区别
4. 使用 `git add <file name>` 将想要添加的文件添加到暂存区准备提交 / `git add .` 加入目录及其子目录下所有符合条件的文件
    + 建议新建.gitignore文件 过滤一些构建文件等不需要的temp files
5. 使用 `git commit -m "log"` 将暂存区的文件提交到本地仓库中，并产生一条commit记录
6. 使用 `git push origin my-feature` 将本地的my-feature分区推送到远程my-feature分支，如果没有会自动创建
    + 如果之前建立过链接可以直接 `git push`
7. 使用pull request将my-feature合并到main （会使用squash and merge，合并所有不同的commit）
8. 删除remote的my-feature分支
9.  回到本地repository，使用`git branch -d my-feature` 删除本地的my-feature分支，因为功能开发完了，不需要了
10. 最后更新local repository的 main分支 使用`git pull`

## 如果上传了新分支后，在merge之前，main分支有了更新（update）
1. 将远程main分支pull下来，更新本地的main分支
2. 切换到my-feature分支  `git checkout  my-feature` 
3. 使用`git rebase main` 在先不管自己的commit情况下将main的更新同步到my-feature分支
   + 大概率可能会有rebase conflict，比如对同一代码同一处都有修改
   + 如果有冲突，就不得不手动解决，比如某一处修改使用哪个版本。建议使用IDE会方便一些
4. rebase成功后，整个代码的 track 看作我在main分支最新的update之后又修改了代码
5. 使用 `git push -f origin my-feature` 因为使用了rebase所以要加上`-f` 强制推送
## 删除远程仓库的某个文件或文件夹
  + 场景：已经在远程仓库上传了某些文件或者文件夹发现上传错了
    + 解决方案 ： `git rm --cached <file/folder>` 然后重新执行push流程同步远程分支

## 恢复到某个版本
+ 场景1 : 一些改动如删除修改后，但没有`add`，使用`git checkout <file name>`
+ 场景2 :  一些改动如删除修改后，也`add`了，但是还没有`commit`，使用`git checkout <target commit id> <file name>`
+ 场景3 :  一些改动如删除修改后，也`add`了，也`commit`了，即退回之前版本，使用`git checkout <target commit id> <file name>`

也可以使用 `git reset -hard/soft/mixed <target commit id>`
  + `hard` 会让暂存区，仓库，工作区的文件都直接同步成回滚的版本号
  + `mixed` 会让工作区的文件回滚但是仓库和暂存区仍是那次错误`commit`的版本
  + `soft` 会让暂存区的文件回滚
  
还可以用 `git revert`
  + 和`reset`相比，他是带注释的回滚，本质上提交一个新的commit，这个commit的作用是回滚到指定的版本，特色是把回滚操作给记录下来了，一切操作有迹可循
## 远程仓库分支回退：
  参考： [远程回退](https://www.cnblogs.com/Super-scarlett/p/8183348.html)
  1. 远程回退的核心就是使用force push，慎用，尤其在公共分支上
  2. 在本地需要回滚的分支上使用 `git reset -hard <previous commit id>`
  3. `git push -f`
     1. 如果在远程分支回滚后要通知所有人，他们“应该强制”同步自己的本地分支和远程分支 `git reset --hard origin/master` 否则他们再一push会把辛苦回滚的版本取消掉 

在公共分支回退要考虑会覆盖别人之前的提交，因为回退了在此之后的commit就查无此人了
所以也可以用 `git revert` 回滚版本，同上一节所说`git revert`命令的好处就是不会丢掉别人的提交，即使你撤销后覆盖了别人的提交，他更新代码后，可以在本地用 reset 向前回滚，找到自己的代码，然后拉一下分支，再回来合并上去就可以找回被你覆盖的提交了。


## 如何让本地的branch和远程branch连接（追踪关系建立）
1. 使用命令`git push --set-upstream origin <local>:<remote>`

## 修正/撤回commit （push之前）
+ 场景1 : commit 马上之后发现文件有小错，改了文件后再次提交，为了不产生冗余的commit log
+ 场景2 : commit 马上之后发现日志信息写错了有小错，为了不产生冗余的commit log

+ 注意 : 只对上次有效
  `git commit --amend -m "<日志注释>"`

## 对commit进行打标签，有关于后续的release
1. 使用命令`git log --oneline` 查看所有commit
2. 使用命令`git tag` 对当前commit打tag
3. 使用命令`git tag <commit id>` 对指定commit打tag
4. 同步到remote时需要单独 push `git push origin <tag id>`
5. 推送全部tag使用 `git push origin --tags`


# 参考视频
[工作流程1](https://www.bilibili.com/video/BV1tm4y1w7Ho?spm_id_from=333.880.my_history.page.click)
[工作流程2](https://www.bilibili.com/video/BV19e4y1q7JJ?spm_id_from=333.880.my_history.page.click)
[Reset VS revert](https://www.bilibili.com/video/BV1hA411m7jL/?spm_id_from=333.337.search-card.all.click&vd_source=7d72d87753aff88f00f4bded7ef264d4)
[恢复版本](https://www.bilibili.com/video/BV1gR4y1C7SW/?spm_id_from=333.880.my_history.page.click&vd_source=7d72d87753aff88f00f4bded7ef264d4)
[恢复版本2](https://www.bilibili.com/video/BV13g411i7yj/?spm_id_from=333.880.my_history.page.click)
[提交修正](https://www.bilibili.com/video/BV1BY411m7MV/?spm_id_from=333.788&vd_source=7d72d87753aff88f00f4bded7ef264d4)