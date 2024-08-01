# Ansible

Ansible是一个自动化运维工具，它可以用来配置服务器、部署应用、管理系统等。Ansible的核心是一个基于Python的SSH协议的轻量级的配置管理工具，它不需要在被管理的服务器上安装客户端，只需要在控制端安装即可。 Ansible的配置文件是YAML格式的，易于阅读和编写。

## 安装

```bash
sudo apt-get install ansible
```

## 配置

对于ansible如何连接到远程服务器，可以配置目录下的hosts文件。这个文件可以包含多个组，每个组包含多个主机。比如：

```ini

[web]
1.1.1.1 

[web:vars]
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa

[db]
1.1.1.2

[db:vars]
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```