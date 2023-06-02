# 概念
## 与虚拟机的不同
一般来说计算机系统可以分为两个部分

1. 应用层
2. 核心层（与硬件通讯）
   
docker是虚拟了应用层，没有自己的OS kernel。而虚拟机是虚拟化了一整个操作系统，包括了核心层。所以这也解释了docker的image是分操作系统的，一般来说在Linux build的 image不适用于在windows上，因为Linux 的application layer无法调用Windows 的os kernel。
但是！Docker desktop 却支持在windows上运行Linux image，其实是因为内部集成了一个轻量级的Linux的发行版，导致了可以让linux 的image可以在windows电脑上运行。

## 安装Docker Desktop到底安装了什么

1. Docker Engine
   核心，server，管理容器和image
2. Docker CLI-Client
   命令行interface，可以和docker server交互
3. GUI Client
   图像化界面与docker server交互

## Docker images是什么，和container有什么关系
1. images是一种可运行的应用artifact，一种集合就像zip文件一样打包了所有需要的东西，比如完整的环境配置信息，任何需要的服务
2. Container是一个运行image实例的地方，可以一个image在不同容器中同时运行
3. Docker Hub 是推荐的docker Registries 可以下载官方或者个人开发者开发的image，同时也是Docker Desktop的默认下载位置




