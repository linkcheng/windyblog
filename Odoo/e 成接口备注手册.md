

1. 在`*api/login/getToken`接口中加入一个新的参数`set_purview`, 该参数你们可以自定义填写用来加盐的,生成出来的Token为一次性使用,强制失效时间120秒,登录成功或者失败都会注销该Token.然后拿这个Token在我们的[Ifchange.com](http://Ifchange.com) 做免登录,这样就能进入E成系统操作入职及offer等了.

2. 正式环境登录URL:[https://www.ifchange.com/?partner=ersoft&partnerToken=test123456](https://www.ifchange.com/?partner=ersoft&partnerToken=test123456)

   partner写ersoft这个固定值就可以了, 是用来我们这边区分客户的.  partnerToken就是set_purview方式得到的token

3. 测试环境的URI地址是:

   http://www.testing2.ifchange.com

   http://tcp.testing2.ifchange.com

   http://www.testing2.ifchange.com/?partner=ersoft&partnerToken=

   | 密码     | 账号             | UID   | NAME |
   | ------ | -------------- | ----- | ---- |
   | abc123 | lilu@esoft.com | 93405 | 易路   |

4. getToken 这个接口有两种方式，一种是带参数 set_purview 与不带参数set_purview。

   带参数 set_purview 表示要做免登录操作，获得的 token 有效期是 120s；

   不带参数set_purview 表示只是做调用接口使用，获得的 token 有效期是 24h。

5. 城市id应该会不会随便变更：

   变动的不会很频繁建议每次都请求.  地址属于我们的基础服务,数据的增改均不会对外提供. 可以向上传递ID,比如市级查不到可查省ID

6. 城市列表支持国外城市，并且经支持中文名称

7. key 

   测试环境:d6e4322ce6d1691818e4b0fc1b56f4ee1aaa47456465290631dc5510acec6412

   正式环境:13161ac1494466fdfc90a8d926e4a1c4fc0e2ee77f8045bb0d1d459a359a8f31

8. 通过用户名密码登录的方式查看已发布职位的url是https://www.ifchange.com/position?organization=0 


通过免登录方式查看已发布职位的url应该是什么

是不是可以这样理解：用partner=[partnerId]&partnerToken=[Token] 的方式就是免登录到你们的系统，但是

https://www.ifchange.com/position?organization=0&partner=ersoft&partnerToken=qazwsxec123 这种方式不能实现直接免登录并且直接跳转到查看已发布职位的页面

#### 需求确认

1. **一般配置改到第三方联通配置统一管理**。（API的token单独处理）

   业务逻辑b：括号里的逻辑需要解释

   业务逻辑c：老的逻辑需要更新成新的。

   业务逻辑d：（得到职位id）改为（得到e成返回的职位id）

   position id 名字需要明确为e成的position id。 

   需要确认e成或者客户会不会改position id 

   **city id map确认会不会修改。和e成确认方案**。

   enable_ifchange 去掉，通过模块安装确认位置。

   company name 用 company code，user name 用login

   access token 放参数表。

2. 城市选项

​       国家 省 城市联动