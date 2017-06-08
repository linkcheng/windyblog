## ArchCon

#### 美团移动网络优化

1. 短连：
   1. 域名分合：SLB  server load balance,域名合并；IP 直连
   2. HTTP1.1连接复用
   3. HTTP 三次握手延时  800ms—8000ms
2. 长连：
   1. HTTP2.0: 请求基于 DNS，不同域名的请求需要建立多条连接
   2. 代理长连模式：中转服务器，DNS无依赖，不同域名请求可以服用同一条长连通道：网络协议自定义
      * TCP 通道加密：移动端到中转
      * HTTP 专线：中转到 server
      * 端到 server：公网HTTP通道（备用、日志文件上报等大数据传输）、UDP 通道
      * 多地部署接入点，就近接入点部署中转服务器（海外），幸存者偏差
3. APP 启动接口优化：
   1. 建立 TCP 通道，建立请求队列，等待建立长连，通过长连发送
4. 网络 SDK spark  推送   监控SDK :CAT 监控
   1. 长连难度大，周期长
   2. 收拢网络底层
   3. 使用网路监控 CAT 
   4. 尝试短连优化：域名合并+IP直连
   5. 尝试 HTTP2.0

#### 蚂蚁金服分布式 Java 技术结构性能优化

1. openJDK 
2. 性能调优： GC  JIT
3. speedup= 1 / (F + (1-F) / N), F:fraction of work that is serial,N: number of threads
4. F: synchronized & lock;stop the world
5. profiling: sampling   instrument,性能堆栈，栈顶；ZProfiler, Honest (github)
6. JVM in memory:
   1. java heap
   2. threads
   3. just in time (JIT) complier
   4. JNI
   5.  direct java.nio.ByteBuffers
   6. Java runtime data
7. GC
   1. 每个worker配置不同的gc
   2. heap size
   3. GG paragramer
8. JIT 
   1. JITWatch
9. 分布式JAVA
   1. 问题：rpc，序列化，反序列化
   2. 1:N 部署模式，共享 JVM（资源隔离）

#### 携程高可用架构的演变和迭代

1. 运维
   1. 集群策略
   2. FullDR
   3. DBA  网状互备。SQL + NoSQL
   4. Noc：订单监控、CAT 监控
2. 框架
   1. SOA & Gateway
      1. SOA 治理平台
      2. H5 Gateway
   2. 发布系统
      1. 回退
      2. 刹车
      3. 切换
   3. 消息队列
      1. partition 有序
      2. 异步补偿
      3. 消息生命周期跟踪
   4. 配置管理
3. 应用
   1. preloading & layerloading
   2. sharding
      1. 分布式计算
      2. 分片存储
   3. 熔断 限流 降级
      1. 熔断 server 不影响前端
      2. 限流：队列
   4. 跨语言解释器
4. auth 验证、反爬，共享登录态
5. userprofile
   1. 组成
      * 注册、采集、计算（kafka+storm）、存储（redis、mysql、Hive）、查询、监控（校验）

#### 手淘 AR/VR 技术框架演进

1. AR/VR 开发
   1. 3D 渲染，openGL、面向GPU、过程式、图形学数学
   2. 游戏引擎
2. Java/OC 层合并 3D/AR/VR 接口
   1. Redim
   2. webGL

#### 点融支付系统的演化之路

1. 实现不统一，扩展性
2. 业务逻辑太靠代码固化
3. 需要服务化
4. 支付服务：
   1. 无状态、包含以及环境不感知
   2. 基于领域模型驱动的模块化设计
   3. 微架构：CQRS & Event Sourcing  (SQLRS:非结构化数据存储)
   4. 基于事件驱动开发，异步（消息中心，插件式处理）
   5. serverless & lambda 架构
   6. 分布式总账：blockchain & corda

#### 新达达账户系统演变

1. 账户系统的职责

   1. 业务系统轻松调用
   2. 支持出账、入账、转账
   3. 记录账户交易流水
   4. 自由结算
   5. 各维度报表
   6. 安全稳定

2. 账户系统的演变

   1. 数据库字段阶段（需求简单，不过度设计，不知道该设计成什么样，日单量小于1000）怎么简单怎么做

   2. 采购第三方系统阶段（日小于10W）业务模式规则，扩张平缓

   3. 借鉴第三方系统，照葫芦画瓢阶段（日小于100W）

      * 账户服务
      * 交易服务
      * 钱包服务
      * 管理平台

      1. 减少全局事务
      2. 消息一致性
      3. 分库分表
      4. 正向异步，异向同步
      5. 满足最小实现原则
      6. 业务无感

   4. 模块服务化阶段（日订单200+W）

      1. 前期路子可以野一点，后期业务要合规
      2. 模块职责专一
      3. 设计自己的模块，而非堆代码
      4. 问题定位难

   #### 饿了么客服平台系统架构

   1. 客服CRM-复杂业务对接
   2. 即时通信-高并发高吞吐
      1. 客户端加速-http/2.0  Server Push
      2. 减少消息链路-gateway
      3. 高效的服务器通信-grpc，protobuffer高效序列化
      4. 无锁队列 - disruptor
      5. 优化重连和探活效率
      6. 精简数据包大小
      7. 离线消息
   3. 机器人客服-智能化水平的考验

#### 如何成为一名独一无二的优秀架构师

1. 如何独一无二
2. 捷径
   1. 磨炼，经验
   2. 对人的管理、对机器的管理
   3. 行业背景积累
3. 陌生问题
   1. 跟懂行的人学习
   2. 让贤
4. 修炼
   1. 以小见大，需要精一个点
   2. 运维、框架、沟通
   3. 知识不够用就要学习