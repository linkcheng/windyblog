# ODOO的重要对象ENVIRONMENT (ENV) 简析

Environment 是 odoo 中操作db的总句柄，以下几种方式可以获得：

1. 在 8.0中，对于继承了Model的类来说可以直接通过self.env得到 Environment
2. 在请求的 Controller 可以通过 request.env()得到 Environment
3. 通过模型类或模型类对象获取，cls.env、product.env

eg 一些常用上下文参数：

- 当前用户　
  self.env.user
- 当前用户id
  self.env.uid
- 当前语言代码
  self.env.lang
- 当前数据库连接
  self.env.cr

Environment用途示例

- 利用 env[model] 获取模型类对象
  1. self.env['ir.model'].search([('state', '!=', 'manual')])
- 利用 env.cr 执行sql语句
  1. self.env.cr.execute(query, (value,))


对于扩展现有模块，（继承机制）即使是对于现有的模块，推荐的做法也是通过新建一个模块来达到扩展和修改现有模块的目的。具体方法就是在python中的类里面使用 **_inherit** 属性。这标识了将要扩展的模块。新的模型继承了父模型的所有特性，我们只需要声明一些我们想要的修改就行了。通过这种继承机制的修改可从模型到视图到业务逻辑等对原模块进行全方位的修改。实际上，Odoo模型在我们定义的模型之外，它们都在**注册中心**注册了的，所谓全局环境的一部分，可以用 **self.env[model name]** 来引用之。比如要引用 res.partner 模型，我们就可以写作self.env['res.partner'] 。


​				
​			
​		
​	
