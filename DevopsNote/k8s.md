# k8s层级
    - deploment
      - replicasets
        - Pod（container）

# ctl command

![alt text](kubectlCommand-1.png)
![alt text](kubectlCommand-2.png)

# Yaml file
Yaml file 是用来定义k8s资源的文件，可以通过 `kubectl apply -f filename.yaml` 来创建资源
每个文件可以包含三个部分：
1. metadata : 包含资源的名字，namespace，labels等信息
2. spec : 包含资源的配置信息，比如容器的镜像，端口，环境变量等
3. status : 包含资源的状态信息，由k8s自动填充, 是k8s自愈的基础，它在运行中会被k8s自动更新并且和spec保持一致，如果不一致就会被k8s自动修复。信息来源于k8s的apiserver中的etcd数据库。

因为是Yaml文件，所以需要严格遵循Yaml的语法规则，比如缩进，空格等。

```yaml
##
