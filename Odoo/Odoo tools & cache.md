# Odoo tools & cache (~/proj/zhengl/odoo/openerp/tools)

1. ormcache， ormcache context，ormcache multi

orm 缓存，避免频换search

@tools.ormcache_multi()

tools.cache.py, odoo lru 算法

对方法的缓存，根据方法名，参数集（可配置）生成 key ，判断是否从缓存中取数据

2. 什么是缓存

为解决性能问题

3. KVDB 持续化存储，如 redis；支持多种数据结构
4. 缓存类型：数据库类型，文件类型，内存缓存
5. 缓存的置换存略：LRU， FIFO， LFU 。。。
6. 数据库缓存，应用层缓存，页面缓存，代理服务器缓存，CDN 缓存
7. 设计缓存， KV结构，hashtable
8. er.base.rank
9. Odoo会话缓存，Ormcache 缓存，排行缓存，业务缓存
10. 继承 dogpile.cache 的 region 增加特殊的sget。