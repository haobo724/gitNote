# GitLab 随记
## GitLab 权限
一般来说main/master分支是被保护的，developer无法对整个分支进行merge或者commit，需要在设置-》repository 内修改设置，或者提升某个用户的权限到maintainer及以上
## 多账户管理

**自己保留private key， 服务端保存public key
**

需要在.ssh文件夹新建一个config文件（无后缀）
添加如下配置
``` shell
Host github.com                 
    HostName github.com
    IdentityFile C:\Users\94836\.ssh\id_rsa
    PreferredAuthentications publickey
    User haobo724


Host gitzhang
    HostName github.com
    IdentityFile C:\Users\94836\.ssh\zhang
    PreferredAuthentications publickey
    User mangomochi-killer
``` 
host 为hostName的别名，不可重复，通过这个识别，是谁上传的（待定）
