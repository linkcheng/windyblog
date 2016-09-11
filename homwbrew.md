# 安装homebrew&postgresql

## 安装 brew

`ruby -e "$(curl http://gitlab.eroadsoftware.com:8000/internal_practice/homebrew_install/raw/eroad_master/install)" `

`sudo easy_install pip`
`sudo pip install --upgrade distribute`
`mkdir ~/.pip`
`touch ~/.pip/pip.conf`
`echo -e "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted`

`host=mirrors.aliyun.com" > ~/.pip/pip.conf`
`brew install openssl`
`brew link openssl —force`  # warning refusings
`brew install python --with-brewed-openssl`

**重新开一个teminal**



## 安装postgresql

`brew install postgresql`
创建postgreSql数据库:
`initdb /usr/local/var/postgres  # don't need to run, because this is created by last commondline`
启动服务：
`pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start`
停止服务:
`pg_ctl -D /usr/local/var/postgres stop -s -m fast`
自动启动服务，9.4.0按需修改
`mkdir -p ~/Library/LaunchAgents`
`cp /usr/local/Cellar/postgresql/9.4.0/homebrew.mxcl.postgresql.plist ~/Library/LaunchAgents/`
`launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist`
删除自动启动服务:
`launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist`
创建用户:
`createuser -d -a -P postgres`


打开 sublime text3 后按快捷键 control+` 后下面会出来东西，然后输入如下命令。

`import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())`

快捷键command+shift+p后会出来列表，找到Package Control:Install Package


Odoo环境依赖
在git.ersoft.cn上找到[odoo基础项目](http://git.ersoft.cn/projects/ODOO)
`pip install -r requirements.txt`

Odoo9创建新数据库报错： Could not execute command lessc
ubuntu解决办法：sudo apt-get install node-less node-clean-css
Mac 方法：
在nodejs.org下载安装 node-v5.1.0.pkg
`sudo npm install -g less`
`sudo npm install -g less-plugin-clean-css`


ehr项目其他依赖
`pip install pdfkit ffmpy celery xmltodict openpyxl jieba pycrypto simplejson asteval xlrd`
