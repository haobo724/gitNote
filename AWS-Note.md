# 基础概念

- root用户：拥有AWS账户的完全访问权限，可以访问所有资源 和Linux一样
- IAM用户：拥有AWS账户的部分访问权限，可以访问指定资源，由root用户创建,在创建时会有一个访问密钥，用于通过AWS CLI访问AWS资源，在创建完成后有唯一一次机会下载这个密钥，csv格式，如果丢了，只能删除重新创建。
- VPC：Virtual Private Cloud，虚拟私有云，云端实体机，EC2实例，数据库等资源都在VPC中
- 子网：subnet，根据VPC的防火墙配置，子网根据访问性质划分，公有子网和私有子网
  - 子网掩码： 举例172.31.15.0/20，20表示前20位是网络地址，后12位是主机地址 ， 从这里可以简单计算 11111111 11111111 00001111 00000000 = 172.31.15.0 前20位锁死，后12位可以变化，所以可分配的IP地址是2^12-2=4094个，也就是范围从 172.31.0.1 - 172.31.15.254，其中0和255分别是网络地址和广播地址，不可分配 

## AWS CLI
 - 安装参考官网
 - 配置
   `aws configure`
   - 输入access key ID
   - 输入secret access key
   - 输入region
   - 输入output format
   以上信息都在创建IAM用户时生成
   如果只想使用“临时”的某个用户可以通过设置环境变量来实现
    `export AWS_ACCESS_KEY_ID=xxxx`
    `export AWS_SECRET_ACCESS_KEY=xxxx`
  - 简单语法
    - `aws command-name --option-name value`
      - filters : 筛选符合特征的资源
        - `--filters "Name=tag:Name,Values=MyInstance"`
        - Name和Values是固定的，tag:Name是筛选的特征，MyInstance是特征的值
      - query ： 筛选特定的信息，只显示这些信息
        - `--query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,Tags[?Key=='Name'].Value]"`
      - 
### 设置安全组
   `aws ec2 authorize-security-group-ingress --group-id sg-0a8288ea515970965 --protocol tcp --port 22 --cidr 37.4.228.119/32`
### 创建key-pair
   `aws ec2 create-key-pair --key-name MyKeyPair --output text > MyKeyPair.pem`
 - aws ec2 run-instances
   --image-id ami-0346fd83e3383dcb4
   --count 1
   --instance-type t2.micro
   --key-name MyKPCli
   --security-group-ids sg-0a8288ea515970965 
   --subnet-id subnet-03b57da1373d0191b

### 创建策略
``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["iam:ChangePassword"]
            ,
            "Resource": ["arn:aws:iam::381492097429:user/${aws:username}"]
        },
        {
            "Effect": "Allow",
            "Action": ["iam:GetAccountPasswordPolicy"],
            "Resource": "*"
        }
    ]
}
```
`aws iam create-policy --policy-name changePwd --policy-document file://aws-changeword-policy.json`
  