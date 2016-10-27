# 如何创建你自己的 Python 包

title:  如何创建你自己的 Python 包

author:  LinkCheng

permalink: how-to-write-your-own-python-packages

keywords: Python, Package Management

***

## 概述
Python 是一门精妙绝伦的语言，就像一杯美酒愈久弥香。然而打包却是它最薄弱的环节之一。这是社区中众所周知的事实。当然，这些年来关于包的安装、导入、使用以及创建都有所改善，但是它仍然不能和像从 Python 的缺点中吸取了很多教训的 Go 和 Rust 这样的新语言，还有其他更加成熟的语言相媲美。

在本教程中，你将会学到创建以及分享自己的包的所需要的一切知识。想要了解关于 Python 包的背景知识，请阅读[如何使用 Python 包](http://code.tutsplus.com/tutorials/how-to-use-python-packages--cms-26000)。

## 项目打包
打包一个项目是一个需要你创建一系列条理清晰的 Python 模块和其他可能用到的文件，并且把它们放到一个很容易使用的结构当中去的过程。你不得不考虑各种各样的事情，如对其他包的依赖关系，内部结构（子包），版本管理，目标受众以及包的形式（源码文件和/或二进制文件）。

### 示例
下面从一个简单的例子开始。[Conman](https://github.com/the-gigi/conman/tree/master/conman) 包是一个管理配置的包。它支持多种文件格式，以及使用 [etcd](https://coreos.com/etcd) 的分布式配置。

一个包的内容通常存储在一个目录中（尽管通常也会把子包分离在不同的目录下下），并且有时候会放在自己的 git 仓库下，比如当前我们这种情况。

根目录下包含各种配置文件（`setup.py` 是必须的也是最重要的），代码本身通常在一个其名称是包名的子目录下，当然最好能有一个测试模块。以下是 “conman" 库的目录结构：
```
> tree
 
.
 
├── LICENSE
 
├── MANIFEST.in
 
├── README.md
 
├── conman
 
│   ├── __init__.py
 
│   ├── __pycache__
 
│   ├── conman_base.py
 
│   ├── conman_etcd.py
 
│   └── conman_file.py
 
├── requirements.txt
 
├── setup.cfg
 
├── setup.py
 
├── test-requirements.txt
 
├── tests
 
│   ├── __pycache__
 
│   ├── conman_etcd_test.py
 
│   ├── conman_file_test.py
 
│   └── etcd_test_util.py
 
└── tox.ini
```

来快速浏览下 `setup.py` 文件。它从 [setuptools](http://pythonhosted.org/setuptools) 库中导入两个函数，分别是： `setpup()` 与 `find_packages()` 。接下来，调用 `setup()` 函数并且使用 `find_packages()` 的返回值作为其中的一个参数。

```python
from setuptools import setup, find_packages
 
 
 
setup(name='conman',
 
      version='0.3',
 
      url='https://github.com/the-gigi/conman',
 
      license='MIT',
 
      author='Gigi Sayfan',
 
      author_email='the.gigi@gmail.com',
 
      description='Manage configuration files',
 
      packages=find_packages(exclude=['tests']),
 
      long_description=open('README.md').read(),
 
      zip_safe=False,
 
      setup_requires=['nose>=1.0'],
 
      test_suite='nose.collector')
```

以上看起来稀松平常。`setup.py` 文件不过是一个普通的 Python 文件，你可以让它做任何你想让它做的事，不过它的主要任务是通过适当的参数配置然后调用 `setup()` 函数，因为在你安装包时，它会被各种工具以一种标准的方式调用。下节中将会展开详细信息。

##配置文件
除了 setup.py，还有一些其他可选的配置文件，在这里罗列出来，一并介绍一下它们各自的使用目的。

### Setup.py
`setup()` 函数采用大量像运行各种命令一样的命名参数来控制包安装的多个方面。当上传你的包到仓库时，有些参数用来指定搜索和过滤的元数据。

* name：包的名称（以及它将如何在 PYPI 中被列出来）
* version：它对保持适当依赖关系管理有决定性作用
* url：包的 URL，通常是 GitHub 或者是 readthedocs 的 URL
* packages：所包含的子包的列表；find_packages() 函数会辅助获取
* setup_requires：这里需要详细说明依赖关系
* test_suite：测试时需要用到的工具

该 `long_description` 在这里设置为 README.md 文件，这是有事实的单一来源的最佳实践。

### Setup.cfg
Set.up 文件还提供了一个命令行界面来运行各种命令。例如，要运行单体测试，可以输入：`python setup.py test`
```
running test
 
running egg_info
 
writing conman.egg-info/PKG-INFO
 
writing top-level names to conman.egg-info/top_level.txt
 
writing dependency_links to conman.egg-info/dependency_links.txt
 
reading manifest file 'conman.egg-info/SOURCES.txt'
 
reading manifest template 'MANIFEST.in'
 
writing manifest file 'conman.egg-info/SOURCES.txt'
 
running build_ext
 
test_add_bad_key (conman_etcd_test.ConManEtcdTest) ... ok
 
test_add_good_key (conman_etcd_test.ConManEtcdTest) ... ok
 
test_dictionary_access (conman_etcd_test.ConManEtcdTest) ... ok
 
test_initialization (conman_etcd_test.ConManEtcdTest) ... ok
 
test_refresh (conman_etcd_test.ConManEtcdTest) ... ok
 
test_add_config_file_from_env_var (conman_file_test.ConmanFileTest) ... ok
 
test_add_config_file_simple_guess_file_type (conman_file_test.ConmanFileTest) ... ok
 
test_add_config_file_simple_unknown_wrong_file_type (conman_file_test.ConmanFileTest) ... ok
 
test_add_config_file_simple_with_file_type (conman_file_test.ConmanFileTest) ... ok
 
test_add_config_file_simple_wrong_file_type (conman_file_test.ConmanFileTest) ... ok
 
test_add_config_file_with_base_dir (conman_file_test.ConmanFileTest) ... ok
 
test_dictionary_access (conman_file_test.ConmanFileTest) ... ok
 
test_guess_file_type (conman_file_test.ConmanFileTest) ... ok
 
test_init_no_files (conman_file_test.ConmanFileTest) ... ok
 
test_init_some_bad_files (conman_file_test.ConmanFileTest) ... ok
 
test_init_some_good_files (conman_file_test.ConmanFileTest) ... ok
 
 
 
----------------------------------------------------------------------
 
Ran 16 tests in 0.160s
 
 
 
OK
```

Setup.cfg 是一个可以将包含默认选项命令传递给 `setup.py` 的 INI 格式的文件。在这里， setup.cfg 包含 `nosetests` （刚才运行的单体测试 ）的一些选项。

```
[nosetests]
 
verbose=1
 
nocapture=1
```

### MANIFEST.in
虽然此文件不包含从属于内部包目录文件，但你仍然可以把那些文件包含在内。这些都是典型的 `readme` 文件， license 文件和一些类似的文件。`Requirements.txt` 文件非常重要，该文件是用来说明通过 pip 安装其他所需包的必要文件。
下面是 conman 的 MANIFEST.in 文件内容：

```
include LICENSE
 
include README.md
 
include requirements.txt
```

### 依赖关系
你可以在 `setup.py` 中的 `install_requires` 部分和 `requirements.txt` 文件中指定包的依赖关系。Pip 会自动安装在 `install_requires` 声明的依赖包，然而在 `requirements.txt` 中声明的却不会自动安装。要安装这些具体的依赖包，需要执行 `pip install -r requirements.txt` 这条 pip 指令来明确指出。

`Install_requires` 选项旨在指定在主版本中最小限度的或者较抽象的依赖包。而在 requirements.txt 文件中更多的是与次版本紧密相连的具体的依赖包。

这是 conman 的 requirements 文件。可以看出，所有版本号都是固定的，这也就意味着，当所依赖的包中有一个进行了升级或者引入了一些变化就会破坏 conman，对其产生一些负面影响。

```
PyYAML==3.11
 
python-etcd==0.4.3
 
urllib3==1.7
 
pyOpenSSL==0.15.1
 
psutil==4.0.0
 
six==1.7.3
```

然而把版本号固定写死却提供了可预测性，并且这样会让人觉得心安。当很多人在不同时间段安装你的包时，这点显得尤为重要。如果不固定下来，每个人在安装包时将会得到基于不同版本的依赖关系。当然，把版本号固定下来也会暴露一些缺点，比如当你跟不上依赖包的开发进度，你将会陷入版本老化，表现不佳甚至是易受攻击的境地。

起初我是在 2014 年写的 conman，当时并没有太在意关于版本一些事情。不过现在，当我写这篇教程时，我不得不更新所有的依赖包，因为几乎每一个依赖项都有了很大程度的改进。

## 发布
你可以发布源码文件也可以发布可执行文件。这两种情况以下我都会涉及到。

###源码发布
通过 `python setup.py sdist` 命令来创建源码发布文件。以下是创建 conman 的输出信息：
```
> python setup.py sdist
 
running sdist
 
running egg_info
 
writing conman.egg-info/PKG-INFO
 
writing top-level names to conman.egg-info/top_level.txt
 
writing dependency_links to conman.egg-info/dependency_links.txt
 
reading manifest file 'conman.egg-info/SOURCES.txt'
 
reading manifest template 'MANIFEST.in'
 
writing manifest file 'conman.egg-info/SOURCES.txt'
 
warning: sdist: standard file not found: should have one of README, README.rst, README.txt
 
 
 
running check
 
creating conman-0.3
 
creating conman-0.3/conman
 
creating conman-0.3/conman.egg-info
 
making hard links in conman-0.3...
 
hard linking LICENSE -> conman-0.3
 
hard linking MANIFEST.in -> conman-0.3
 
hard linking README.md -> conman-0.3
 
hard linking requirements.txt -> conman-0.3
 
hard linking setup.cfg -> conman-0.3
 
hard linking setup.py -> conman-0.3
 
hard linking conman/__init__.py -> conman-0.3/conman
 
hard linking conman/conman_base.py -> conman-0.3/conman
 
hard linking conman/conman_etcd.py -> conman-0.3/conman
 
hard linking conman/conman_file.py -> conman-0.3/conman
 
hard linking conman.egg-info/PKG-INFO -> conman-0.3/conman.egg-info
 
hard linking conman.egg-info/SOURCES.txt -> conman-0.3/conman.egg-info
 
hard linking conman.egg-info/dependency_links.txt -> conman-0.3/conman.egg-info
 
hard linking conman.egg-info/not-zip-safe -> conman-0.3/conman.egg-info
 
hard linking conman.egg-info/top_level.txt -> conman-0.3/conman.egg-info
 
copying setup.cfg -> conman-0.3
 
Writing conman-0.3/setup.cfg
 
creating dist
 
Creating tar archive
 
removing 'conman-0.3' (and everything under it)
```

正如你看到那样，由于缺失以 README 为标准前缀的文件而被警告，不过由于我个人喜欢 Markdown，所以我用 "README.md" 代替。除此之外，所有的包源文件以及额外附件文件都被包含进去。于是，在 `conman.egg-info` 目录下生成了一个元数据的文件群。最后，在 `dist` 子目录下生成一个叫 `conman-0.3.tar.gz` 的 tar 压缩包文件。

安装这个包需要一个构建的过程（即使这是一个纯 Python 包）。你只需给出压缩包的路径，然后就能使用 pip 安装它。例如：

```
pip install dist/conman-0.3.tar.gz
 
Processing ./dist/conman-0.3.tar.gz
 
Installing collected packages: conman
 
  Running setup.py install for conman ... done
 
Successfully installed conman-0.3
```

Conman 被安装在 site-packages 目录下，并且可以像其他包一样导入使用:

```
import conman
 
conman.__file__
 
'/Users/gigi/.virtualenvs/conman/lib/python2.7/site-packages/conman/__init__.pyc'
```

（译者注：如果读者跟译者一样是使用 Ubuntu 系统或者其他 Debian 系统，请参考 [Debian Python Wiki](https://wiki.debian.org/Python) 。简单来说就是 dist-packages 取代了 site-packages。从 Debian 安装包安装的第三方的 Python 软件被安装到 dist-packages，而不是 site-packages。这是为了减少系统自带 Python 和你手动安装的 Python 之间的冲突。dist-packages 是 Debian 特定惯例，这也存在于像是 Ubuntu 上。如果使用 Debian 软件管理器安装，模块将被安装到 dist-packages，路径是：/usr/lib/python2.7/dist-packages。如果使用 easy_install 和 pip 安装软件包，它们也使用 dist-packages，但路径是：/usr/local/lib/python2.7/dist-packages。)

## Wheels 
Wheels 是相对比较新的包装 Python 代码与 C 扩展的方法。它取代过去 egg 格式的文件。有几种格式的 wheels：纯 Python wheels、平台 wheels 以及通用 wheels。像 conman 一样的纯 Python wheels 包不包含任何 C 扩展代码。

平台 wheels 包含 C 扩展代码。通用 wheels 是同一份代码同时兼容 Python 2 和 Python 3 的纯 Python wheels（它们甚至不需要 2to3 转换）。如果你有需要同时兼容 Python 2 和 Python 3 （这变得越来越重要）的纯 Python 包，你只需要用通用 wheels 构建一次，这足以替代用 Python 2 wheels 和 Python 3 wheels 各自构建。

如果你的包有 C 扩展代码，那么你就必须构建使用每个平台的平台 wheel。wheels 特别是对 C 扩展包的巨大优势是不再需要在目标机器上安装编译器以及所需要的依赖库。Wheel 包含一个内置的包，所以构建时不会失败。由于使用直接拷贝模式，使得安装非常迅速。使用像 Numpy 和 Pandas 这样的科学计算库的的用户能真正体会到这一点，因为安装这些包需要花费大量时间，并且一旦缺少某些库文件或者编译器配置不恰当就会导致安装失败。

创建纯 wheels 或者平台 wheels 的指令是：` python setup.py bdist_wheel `。

Setuptools 引擎提供了 `setup()` 函数，这个函数会自动的检测是需要纯 Python 还是平台 Wheel 。

```
running bdist_wheel
 
running build
 
running build_py
 
creating build
 
creating build/lib
 
creating build/lib/conman
 
copying conman/__init__.py -> build/lib/conman
 
copying conman/conman_base.py -> build/lib/conman
 
copying conman/conman_etcd.py -> build/lib/conman
 
copying conman/conman_file.py -> build/lib/conman
 
installing to build/bdist.macosx-10.9-x86_64/wheel
 
running install
 
running install_lib
 
creating build/bdist.macosx-10.9-x86_64
 
creating build/bdist.macosx-10.9-x86_64/wheel
 
creating build/bdist.macosx-10.9-x86_64/wheel/conman
 
copying build/lib/conman/__init__.py -> build/bdist.macosx-10.9-x86_64/wheel/conman
 
copying build/lib/conman/conman_base.py -> build/bdist.macosx-10.9-x86_64/wheel/conman
 
copying build/lib/conman/conman_etcd.py -> build/bdist.macosx-10.9-x86_64/wheel/conman
 
copying build/lib/conman/conman_file.py -> build/bdist.macosx-10.9-x86_64/wheel/conman
 
running install_egg_info
 
running egg_info
 
creating conman.egg-info
 
writing conman.egg-info/PKG-INFO
 
writing top-level names to conman.egg-info/top_level.txt
 
writing dependency_links to conman.egg-info/dependency_links.txt
 
writing manifest file 'conman.egg-info/SOURCES.txt'
 
reading manifest file 'conman.egg-info/SOURCES.txt'
 
reading manifest template 'MANIFEST.in'
 
writing manifest file 'conman.egg-info/SOURCES.txt'
 
Copying conman.egg-info to build/bdist.macosx-10.9-x86_64/wheel/conman-0.3-py2.7.egg-info
 
running install_scripts
 
creating build/bdist.macosx-10.9-x86_64/wheel/conman-0.3.dist-info/WHEEL
```

查看 `dist` 目录，就会发现一个纯 Python wheel 被创建出来：
```

ls -la dist
 
 
 
dist/
 
total 32
 
-rw-r--r--  1 gigi  staff   5.5K Feb 29 07:57 conman-0.3-py2-none-any.whl
 
-rw-r--r--  1 gigi  staff   4.4K Feb 28 23:33 conman-0.3.tar.gz
```

文件 conman-0.3-py2-none-any.whl 有几个组成部分：包名，包的版本，Python 版本，平台版本，最后是后缀名 whl。

打造通用包时，仅需要添加 `--universal` 选项，如：`python setup.py bdist_wheel --universal`。

生成的文件名是“conman-0.3-py2.py3-none-any.whl”。

值得注意的是，确保你的代码能兼容 Python 2 和 Python 3 依然是你的责任，即使创建通用型包，也不要过于依赖 wheels 工具。

##结论
构建你自己 Python 包需要处理大量的工具，指定大量元数据，并仔细考虑依赖关系以及目标受众。但这一切都是值得的。

如果你写的代码很有用并且正确打包，那么人们将能轻松地安装它，并从中受益。

***

[点此查看原文链接](http://code.tutsplus.com/tutorials/how-to-write-your-own-python-packages--cms-26076)。

[Python 翻译组](https://github.com/PythonTG)是EarlGrey@编程派发起成立的一个专注于 Python 技术内容翻译的小组，目前已有近 30 名 Python 技术爱好者加入。翻译组出品的内容（包括教程、文档、书籍、视频）将在编程派微信公众号首发，欢迎各位 Python 爱好者推荐相关线索。推荐线索，可直接在编程派微信公众号推文下留言即可。
