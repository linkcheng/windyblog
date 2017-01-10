# Postman 说明

Postman是一种网页调试与发送网页http请求的chrome插件。我们可以用来很方便的模拟get或者post或者其他方式的请求来调试接口。

### 基本使用方法

我看的是发送请求的这个，postman接口分为两个区域，左边的是侧边栏，有的是历史和收藏，右边是请求构造的地方，见下图： 
![请求构造的主页面](http://img.blog.csdn.net/20151218162441182)

URL 
url是最重要的你要设置的那个请求。URL会存储之前的urls，会在你输入的时候自动提示。当你点击URL 后面的params的时候，会粗线一个键值对输入的地方。（键值对也会在你输入url上面参数的时候，生成的） 
![url](http://img.blog.csdn.net/20151218163158932)

Headers 
点击Header这个标签会出现headers的键值对 ，你可以设置任何的header name，当你输入name的时候，会出现下拉提示，value值同样也可以出现自动下拉提示。 
![Headers](http://img.blog.csdn.net/20151218165128110)

说明：在这里以一个提交多层嵌套的json数据格式的post请求为例。

如：

```
 1 data=
 2 {
 3     "xxx": 
 4   {
 5         "xxx": "xxxxxxxxxxx",
 6         "xxx": "xxxxxxxxxxx"
 7     },
 8     "aaa": "xxxxxxxxxxx",
 9     "bbb": "xxxxxxxxxxx",
10     "ccc": "xxxxxxxxxxx"
11 }
```

1、在chrome中安装好postman插件后，通常会在桌面上生成一个Postman的快捷方式，再次打开它时可以直接通过快捷方式也可以在chrome浏览器中的应用中打开它，我们会看到如下界面：

![img](http://img2.tuicool.com/mMNVzyR.png!web)

2、打开后，在红圈里面输入需要测试的接口地址，选择post方式，然后在下面的Headers中手动添加一个相应的键值。这个很关键，一定要填写正确。

（如：json格式的提交数据需要添加：Content-Type ：application/x-www-form-urlencoded，否则会导致请求失败）

**POST json 请求格式：**

在header中添加**Content-Type:application/json**

body中选择 **raw** 格式，然后选择 **JSON（application/json）**

如图：

![img](http://img2.tuicool.com/bE3iyi.png!web)

3、选择Body选项卡，然后选中row，在编辑框中输入你需要提交的参数即可：

![img](http://img0.tuicool.com/VZNVRf.png!web)

4、点击Send即可提交请求，然后在下面查看请求结果，并且可以以Pretty、Raw、Preview三种方式查看。如图：

![img](http://img2.tuicool.com/IBnQFja.png!web)

注：本篇文档只是简单举了个列子满足我们日常测试即可，更多的细节可登录[Postman官方网站](https://www.getpostman.com)



1. Get请求

   在地址栏里输入请求url：http://localhost:9998/api/user

   选择“GET”方式

   点击"Url params",添加url params key:id , value:1

   点击“send”得到json数据如下：

   [![如何在Chrome下使用Postman进行rest请求测试](http://f.hiphotos.baidu.com/exp/w=500/sign=a7e730a418178a82ce3c7fa0c602737f/562c11dfa9ec8a1346e69d88f103918fa1ecc0de.jpg)](http://jingyan.baidu.com/album/90808022ff18defd91c80f9a.html?picindex=7)

2. ​

   如果想要Post请求：

   在地址栏里输入请求url：http://localhost:9998/api/user/1

   选择“POST”方式，

   点击"application/x-www-form-urlencoded",

   添加key:name , value:baidu-lulee007

   添加key:sex , value:man

   ​

   [![如何在Chrome下使用Postman进行rest请求测试](http://e.hiphotos.baidu.com/exp/w=500/sign=14041d69ef24b899de3c79385e071d59/d6ca7bcb0a46f21f8235693af0246b600c33ae51.jpg)](http://jingyan.baidu.com/album/90808022ff18defd91c80f9a.html?picindex=8)

3. ​

   注意：请求支不支持post请求是由服务端决定。

   如果服务端需要请求类型为json，需要在“headers”添加

   key:Content-Type   , value:application/json

   ​

   选择“raw”,并添加：

   {

       "id": 1,

       "data": {

           "name": "baidu-lulee007",

           "sex": "man"

       }

   }

   [![如何在Chrome下使用Postman进行rest请求测试](http://a.hiphotos.baidu.com/exp/w=500/sign=0397096a8144ebf86d71643fe9f8d736/d1a20cf431adcbef1efe4e6faaaf2edda2cc9f94.jpg)](http://jingyan.baidu.com/album/90808022ff18defd91c80f9a.html?picindex=9)



[官方文档](https://www.getpostman.com/collection)

[官方教程](https://www.getpostman.com/docs/collections)





