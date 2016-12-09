# Odoo 源码分享

1. domain 解析过程
   1. [('|', a, '|', b, '|', c, d, e)] 先运算 ‘|’ ,c ,d
   2. [('|', a, '|', b, f, e)]
   3. [('|', a, g, e)]
   4. [(h, e)]
2. module 安装卸载
   1. 应用加载过程 Registry.py
   2. openerp.cli.main()   start
   3. command.py
   4. cli.server
   5. loading.py  load_module()