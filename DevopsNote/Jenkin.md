# 安装
用docker!

# 配置

使用build tools有两种方式，一种是在jenkins中安装插件，一种是在docker中安装build tools

$注意$：`使用插件安装则在shell中是找不到的`

## jenkins file with pipeline job

有两种方式，一种是在jenkins中配置，一种是在项目中配置。

注意和git协作时，使用webhook，这样每次git push都会触发jenkins job，如果jenkins job内build阶段包含类似于 update version的参数，那么每次流水线执行完可能会执行push，更新git repo，这样会导致死循环。解决方案可以是在jenkins job中加入判断看push的推送者是谁或者根据commit message来判断是否执行build阶段。

### 在项目中配置
需要建立个Jenkins File 使用的是jenkins file 的groovy语法

``` groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
```

### 在jenkins pipeline中配置

使用的是jenkins的pipeline语法

## Syntax

每个关键词用大括号包裹

变量用`${}` 包裹，如果想在字符串中引用变量，需要用双引号包裹

### 关键字

- environment: 设定环境变量
- agent: 在哪个节点上运行
- stages: 阶段
  - stage: 阶段
  - steps: 步骤
    - sh: shell命令
    - echo: 输出
    - script: 调用groovy脚本 ，这个思路跟html中js和css分离的思路一样
      - Jenkinsfile里的环境变量可以在groovy脚本中直接使用
- tools: 使用安装的tools，比如maven
  
``` groovy
tools {
    maven 'maven3' // 这里的maven3是在jenkins中配置的maven名字
}
```

- parameters: 参数
  
  参数种类有：
  - choice: 选择
  - string: 字符串
  - booleanParam: 布尔
  举例：

  ``` groovy
    parameters {
        choice(name: 'Version', choices: ['A', 'B', 'C'], description: 'Choose A, B or C')
        string(name: 'STRING', defaultValue: 'default', description: 'Enter a string')
        booleanParam(name: 'executeTest', defaultValue: true, description: 'Enable or disable')
    }
    ```

- when: 条件
  - expression: 表达式
  结合parameter举例：

  ``` groovy
    when {
        expression {
            return params.executeTest == true
        }
    }
  ```

- input: 输入
  - message: 提示信息
  - id: id
  - ok: 确认信息
  - parameters: 参数 同上
  - submitter: 提交者
  举例：

  ``` groovy
    input {
        message 'Deploy to production?'
        ok 'Yes'
        parameters {
            choice(name: 'Version', choices: ['A', 'B', 'C'], description: 'Choose A, B or C')
        }
        submitter 'admin'
    }
  ```

- input message: 输入信息,一般是把输入的作为变量，必须是在script中，用`,`分隔各个参数

  举例：

  ``` groovy
    def userInput = input message: 'Do you want to continue?', ok: 'Yes'
  ```

- post: 完成后执行的操作
  - always: 总是执行
  - success: 成功后执行
  - failure: 失败后执行
  - unstable: 不稳定后执行
  - changed: 改变后执行
  - withCredentials: 使用凭证
  - usernamePassword: 用户名密码
  - secretText: 密文
  举例：

    ``` groovy
    withCredentials([usernamePassword(credentialsId: 'my-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
        sh 'echo $USERNAME'
        sh 'echo $PASSWORD'
    }
    ```

### Shared library

jinkeins的共享库，可以把一些公共的方法放在这里，然后在jenkinsfile中调用, 共享库使用groovy语法。

就是编程的思想，把一些公共的方法放在一个地方，然后在需要的地方调用。

#### Example
shared library写法：

shared library为一个git仓库，里面有个vars目录，里面有个groovy文件，这个文件里面有个方法，这个方法就是共享的方法。除此之外还有一个resources目录，里面有一些资源文件。还有一个src目录，里面有package,package是groovy类 。还有lib目录，里面有一些jar包。


src目录下的groovy类写法：

``` groovy
package com.example

class MySharedLibrary implements Serializable {
    def script
    MySharedLibrary(script) {
        this.script = script
    }
    def buildjar_from_shared_library(script) {
        script.echo 'Building..' //注意这里的script是传入的参数
        script.echo " '${script.env.JOB_NAME}'" //注意参数要再加个${}和单引号
    }
}
```

vars目录下的groovy文件写法：

``` groovy
#!/usr/bin/bash groovy
// filename: var/buildjar_from_shared_library.groovy
def call(arg) { //call 是默认保留字
    echo 'Building..'
}

如果是引用src目录下的groovy类，需要在vars目录下的groovy文件中引用
import com.example.MySharedLibrary
def call(arg) {
    new MySharedLibrary(this).buildjar_from_shared_library(arg)
}
```

jenkinsfile 如下（全局）：

``` groovy
@Library('my-shared-library') _ //如果下面的语句是pipeline的话，这个下划线是必须的。
pipeline {
    agent any
   
    stages {
        stage('Build') {
            script {
               buildjar_from_shared_library()
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }

}
```

非全局的jenkinsfile如下：

``` groovy
library identifier: 'my-shared-library@version/branch', retriever: modernSCM(
  [$class: 'GitSCMSource', //在UI里面配置的很类似
   remote: 'url',
    credentialsId: 'credentialId',
  ]
)
@Library('my-shared-library@x.x'#<-这里的x.x是这个Jenkinsfile自定义的) _ //如果下面的语句是pipeline的话，这个下划线是必须的。
pipeline{...}
```

在Jenkinsfile中可以直接引用Jenkins中配置的credentials，直接引用名字即可，通常设置在Jenkinsfile中的环境变量中。

``` groovy

pipeline {
    agent any
    environment {
        MY_CREDENTIALS = credentials('my-credentials')
    }
    stages {
        stage('Example') {
            steps {
                echo "Username: ${MY_CREDENTIALS_USR}"
                echo "Password: ${MY_CREDENTIALS_PSW}"
            }
        }
    }
}
```

## Jenkins运行kubectl 传参问题（Deployment）

注意点，主要是各种凭证验证，很多验证方式取决于k8s运行的平台。

- 在Jenkins中运行kubectl需要安装kubectl，可以在jenkins中安装kubectl插件，也可以在jenkins中安装kubectl，然后在Jenkins中配置kubectl的环境变量。
- 在Jenkins中运行kubectl需要配置好kubeconfig文件，这个文件是k8s的配置文件，在~/.kube/cofig中。
- Jenkins运行yaml文件可能会遇到传参问题，这个时候可以在yaml文件中使用环境变量，然后在jenkins中传参。传参可以使用工具envsubst，这个工具可以替换yaml文件中的环境变量，举例：
  
``` shell
envsubst < file.yaml | kubectl apply -f -
```

- kubectl 在pull docker image时同时也要凭证，这个时候可以使用docker-registry-secret，这个是k8s的secret，可以在k8s中创建，然后在yaml文件中引用。 举例：
  
``` yaml
spec:
containers:
- name: myapp
    image: myapp:latest
imagePullSecrets:
- name: myregistrykey
```

## Jenkins 运行terraform传参问题

Jenkins运行terraform多是在deploy阶段，terraform负责初始化infrastructure，初始化的资源的某些参数不能预先知道，比如服务器IP，这时候就可以结合shell脚本和terraform output进行传参

``` shell
VARIABLES= sh(
    script: "terraform output VARIABLES",
    returnStdout: true
).trim()

```

这样就可以在jenkins中获取terraform output的值，然后传参给下一个阶段。