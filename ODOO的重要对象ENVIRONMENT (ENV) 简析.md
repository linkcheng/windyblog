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