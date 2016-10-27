# Mac 安装 virtualenv 安装使用

## 安装：

1. 打开终端，输入命令：

   ` sudo pip install virtualenv`

没有报错就说明安装成功了。

2. 重启终端输入命令：

   `virtualenv —version`

出现版本号即表示正确安装。

## 使用：

1. 创建一个项目，进入到这个项目的目录下，如项目目录为:

"/Documents/PythonProject/AppDownload"

`cd /Documents/PythonProject/AppDownload`

2. 在这个目录下面创建python的独立运行环境，命名为venv,命令行如下：

`virtualenv --no-site-packages venv`

命令virtualenv就可以创建一个独立的Python运行环境，我们还加上了参数 --no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。

3. 使用新建的Python环境，可以用source进入该环境：

`source venv/bin/activat`

此时你会发现命令行有个(venv)前缀，表示当前环境是一个名为venv的Python环境。

正常安装各种第三方包，并运行python命令：

`pip inatall jinjia2`

4. 退出当前的venv环境，输入deactivate命令：

`deactivate`

你会发现命令行的venv不见了，证明推出了venv环境。 