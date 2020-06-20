# USTC Software 2020 Backend Test

DDL：2020/6/30

## 背景

学校的选课系统太慢了，我们希望能够使用 Django 重写一个能稍微快一点的选课系统。

这次我们要实现一个大幅精简的选课系统。

## 要求

你需要：

1. Fork 此仓库至你的账号。
2. 使用 Django，完成如下所述的功能。
3. 在本文件末尾为前端组的同学撰写一份说明文档，使他们了解你的应用的接口等信息。
4. 发起 Pull Request。（请在 PR 时写上你的姓名、学号）

### 约定

1. 使用 Python 3.6+ 与 Django 3。
   1. Django 3 相对于 2 发生了一些变化，为了避免出现意外情况，请以 Django 3 完成后续的任务与接下来的开发。
   2. 考虑到 Ubuntu 20.04 已经将 Python 3.8 作为默认 Python 版本，我们不会强制要求使用 Python 3.6，并在部署时将采用 Python 3.8。
2. 使用默认的数据库（SQLite）、默认的 HTTP 服务器和默认的端口。
3. 不需要使用 template，不需要编写 HTML 文件。所有接口的返回内容为 JSON。

## 目标功能

### 必须完成的功能

#### 用户账户相关

* 注册与登录账户 x
* 退出账户 x

#### 系统相关

* 列出所有课程 x
* 用户根据课程的`pk`选中课程 x
* 列出用户选中的课程 x
* 退课 x

### 可以选做的功能

#### 用户相关

* 添加年级属性 x
* 某个课程是否学过（参考[Extra fields on many-to-many relationships](https://docs.djangoproject.com/en/3.0/topics/db/models/#extra-fields-on-many-to-many-relationships)）x

#### 系统相关

* 根据年级分类课程 x
* 返回给用户的结果中只展示符合用户年级的课程 
* 添加前置课程，并在结果中返回相对应的前置课程 x
* 更新用户是否学过某个课程 x

> 前置课程即为用户想要选中某个课程，必须要先选中的课程，例如数分A2需要先学数分A1。注意避免循环引用。

### 补充说明

对于添加年级属性，一种方法是创建一个新的 Model，并与 User 绑定 One-to-one 关系（参考 [OneToOneField](https://docs.djangoproject.com/en/3.0/ref/models/fields/#onetoonefield)），在这个 Model 中添加需要的属性。

还有一种方法是，从 `AbstractUser` 继承一个新的 User Model，并在新的 User Model 中添加需要的属性（参考[Substituting a custom User model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model)）。

对于第二种方法，在其他地方引用User时，需要通过 `django.contrib.auth.get_user_model` （参考 [Referencing the User model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model) 得到新的 User Model，或者直接从相应的文件中导入新的 Model。

## 加分项

这些加分项都是值得提倡的良好的开发习惯，因此我们将它们作为加分项。

* 良好的代码风格（如变量命名）会有额外加分
* 良好的注释和文档会有额外加分
* 良好的 Git 提交记录（每次提交有明确的信息）会有额外加分
* 良好的安全性、鲁棒性和可扩展性会有额外加分
* 良好的单元测试有额外加分

## 其它注意事项和提醒

* 对于以上提到的各项功能，最基础的要求是：用户输入正确的请求时，程序可以给出正确的回复。同时，对于用户发起的错误的请求，程序不会受到灾难性的破坏，不会影响其它用户的正常使用（例如，在注册账户时把已有的账户「覆盖」掉是不容许的）。

* 你可以选择将这些功能做得更完善和更安全，具体内容和方式请自行决定，例如检查输入并返回有意义的错误信息等。

* 你可以参考去年的[后端测试题](https://github.com/taoky/USTC-Software-2019-BE-Test)，但请注意，**不要抄袭其他人的代码**，如果某段代码对你编写有帮助，请在注释中写明来源。

* 允许使用任意 PyPI 中的模块，即可以使用 `pip` 命令安装的模块。请在 `requirements.txt` 中添加需要的模块。

* 我们最终的代码会在 Linux 下执行，所以如果你在使用其它操作系统开发，请谨慎使用依赖于特定操作系统的特性。（但这里应该不会出现这种情况）

## 报告（需要完成）

请将你为前端组的同学撰写的报告放在这里。

后面有一个示例

## 一个示例

### 登录

#### URL

`accounts/login`

#### POST

##### 请求参数

| key      | description |
| -------- | ----------- |
| username | 用户名      |
| password | 密码        |

##### 响应参数

| key | description |
| --- | ----------- |
| msg | 返回的消息  |

| status | description    |
| ------ | -------------- |
| 200    | 成功           |
| 401    | 登陆失败       |
| 500    | 服务器内部错误 |

### 补充说明

为节省时间，必须完成的部分需要比较完整的文档，可选完成的部分可以进行简化。

使用 API 文档生成库是允许的，可以不需要完成报告，但需要按照相应的库的要求完成文档的构建，同时需要在报告中说明使用了 API 文档生成库。

Swagger UI：[https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/)

Postman: [https://www.postman.com/api-documentation-generator/](https://www.postman.com/api-documentation-generator/)
