# Linux常用命令

## 1. 基本操作

- ls：查看目录下的文件
- cd：切换目录
  - cd ~：切换到用户主目录
- pwd：显示当前目录
- mkdir：创建目录
- touch：创建文件
- cp：复制文件或目录
  - cp -r：复制目录内所有文件，下同
- mv：移动文件或目录/重命名文件或目录
- rm：删除文件或目录
- cat：查看文件内容
- su 用户名：切换用户
- exit：退出当前用户
- export：设置环境变量(临时)
  - 永久设置环境变量：在/etc/profile或~/.bashrc中添加export 环境变量， 然后执行source /etc/profile或source ~/.bashrc
  - 可以将脚本文件加入到path中，然后直接执行脚本文件

## 2. vim编辑器

  默认是command模式，按i进入编辑模式，按esc退出编辑模式，输入:wq保存并退出，:q!不保存退出

  在command模式下：
  
- <行>G：跳转到指定行
- gg：跳转到文件开头
- G：跳转到文件结尾
- dd：删除当前行
- yy：复制当前行
- p：粘贴
- u：撤销
- /关键字：查找关键字，n查找下一个，N查找上一个
- :set nu：显示行号
  
## 3. 文件/用户权限

Linux 一般有三种用户 root、普通用户、服务用户。
对于用户，一般把用户先添加到组，然后控制组的权限。

- adduser：添加用户
- addgroup：添加组
- usermod -g 组名 用户名：修改用户所属主组
  - usermod -G 组名 用户名：添加用户到附加组
  - usermod -aG 组名 用户名：添加用户到附加组，不会删除原有附加组 ,但都是要重启生效
- gpasswd：修改用户密码
  - d: 删除用户
- groups：查看用户所属组

- ls -l：查看文件权限
  - r：读权限
  - w：写权限
  - x：执行权限
  - d：目录 (first character)
  - l：软链接 (first character)
  - s：socket
  - p：管道
  - c：字符设备 (first character)
  - b：块设备

文件权限分为三组：所有者、同组用户、其他用户 owner group other 缩写为 u g o，或者使用a表示所有用户, 通过+/- 来增加或删除权限，通过=来设置权限

- chmod：修改文件权限
  - chmod 777：所有用户都有读写执行权限 原理为： rwxrwxrwx 111 111 111 即7 7 7
  - chmod 755：所有者有读写执行权限，同组用户和其他用户有读和执行权限 原理为：rwxr-xr-x 111 101 101 即7 5 5
  - chmod 644：所有者有读写权限，同组用户和其他用户有读权限 原理为：rw-r--r-- 原理为110 100 100 即6 4 4
- chown：修改文件所有者
- chgrp：修改文件所属组

## 4. pipe管道

- |：管道符，将前一个命令的输出作为后一个命令的输入
- \>：重定向符，将命令的输出重定向到文件，会覆盖原文件
- \>>：追加重定向符，将命令的输出追加到文件末尾
- <：输入重定向符，将文件作为命令的输入
- 2>：错误重定向符，将错误输出重定向到文件
- &>：将标准输出和错误输出都重定向到文件
- tee：将命令的输出同时输出到屏幕和文件
- xargs：将标准输入转换为命令行参数
- grep：过滤文本，查找关键字
- awk：文本处理工具，可以处理文本文件中的数据
- sed：流编辑器，可以对文本文件进行替换、删除、新增等操作
  
``` shell
# 例子
history | grep 'vim' 
把历史命令中包含vim的命令筛选出来

history | grep 'vim' > vim.txt
把历史命令中包含vim的命令筛选出来并保存到vim.txt文件
```

## shell file

注意空格，shell文件中的空格很重要，不能随意添加或删除空格

- #!/bin/bash：指定解释器
- echo：输出
- read：读取输入
  - -p：提示信息
- $1 $2 ...：获取参数
  - $*：获取所有参数
  - $#：获取参数个数
- if [ condition ]
  then
    command
  fi
- for var in list
    do
        command
    done
- while [ condition ]
    do
        command
    done

- function func_name(){
    command
}

传递密码的技巧:

```shell

echo "password" | docker login --username username --password-stdin

```

## ssh命令

- ssh：连接远程主机
  - `ssh 用户名@主机名`
  - `ssh -p 端口 用户名@主机名`
  - `ssh -i 私钥文件 用户名@主机名`
- ssh-copy-id：将本地公钥复制到远程主机
  - `ssh-copy-id 用户名@主机名`
  - `ssh-copy-id -i 私钥文件 用户名@主机名`
- ssh-keyscan：扫描主机公钥, 防止第一次连接时出现yes/no提示
  - `ssh-keyscan -H 主机名 >> ~/.ssh/known_hosts`
