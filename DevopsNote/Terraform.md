# Terraform

Terraform是一个基础设施即代码工具(Iac)，它允许你定义基础设施的配置文件，然后使用这些配置文件来创建、更新和删除基础设施。Terraform配置文件使用HCL（HashiCorp Configuration Language）编写，它是一种易于阅读和编写的配置语言。terraform是一种声明式的配置语言，这意味着你只需要定义你想要的基础设施，而不需要定义如何实现这些基础设施。

## Syntax

HCL类似于JSON，但是更加人类可读。HCL的基本语法如下：

```hcl
# This is a comment
variable "region" {
  type    = string
  default = "us-west-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

对于不同的平台，需要使用不同的provider，比如AWS，Azure等。在配置文件中，需要指定使用的provider。

```hcl
provider "aws" {
  region = var.region
}
```

在初次使用时需要先初始化terraform，使用`terraform init`命令。初始化完成后，可以使用`terraform plan`命令来查看terraform的执行计划，使用`terraform apply`命令来执行计划。
如果对一个terraform重复执行`terraform apply`命令，terraform会自动检测当前状态和配置文件的差异，然后生成一个执行计划（declarative）

创建资源使用`resource`关键字，资源的类型和名称之间使用空格分隔。资源的属性使用键值对的形式定义。
如果创建资源时需要引用上下文，可以直接使用resource的名称和属性名称.
如果需要查询，则使用`data`关键字.



