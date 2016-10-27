# ODOO8.0新API文档

### odoo新API概述

在odoo8中，api接口分为**traditaional style**和**record style**. traditional style指的就是我们在7中使用的类型,

**def (cr,uid,ids,context)**式的语法.而record style精简了参数,只保留了self和args,形如**def (self,args)**

 __all__ = [

      'Environment',

      'Meta', 'guess', 'noguess',

      'model', 'multi', 'one',

      'cr', 'cr_context', 'cr_uid', 'cr_uid_context',

      'cr_uid_id', 'cr_uid_id_context', 'cr_uid_ids', 'cr_uid_ids_context',

      'constrains', 'depends', 'onchange', 'returns',

  ]

由api.py文件中的定义可以看出,可供使用的有这么多属性．接下来我们一一看看他们的用法．

* Environment:ORM记录的包装类,封装了cr,uid,context等属性,同时提供了注册访问,记录缓存,管理重新计算的数据结构
* Meta:自动装饰traditional style的装饰类，同时实现了对returns装饰的继承
* guess:该装饰标识方法既可以被traditional style调用也可被record style方式调用
* noguess:阻止所有guess的作用
* **model**:装饰record-style方法中的self为记录集
* **multi**:同model,区别在于model中的相当于traditional-style中model.method(cr,uid,args,context=context),而multi为model.method(cr,uid,ids,args,context=context)
* **one**:装饰record-style方法中的self为单一实例,被装饰的方法将会在每一条记录中循环调用，返回一个list结果集，如果和＠returns一块用了,将返回连接的结果．
* **cr**:装饰traditional-style方法,标识将cr作为一个参数
* cr_context:装饰traditional-style方法,标识将cr,context作为参数
* cr_uid:装饰traditional-style方法,标识将cr,uid作为参数
* cr_uid_context:装饰traditional-style方法,标识将cr,uid,context作为参数
* cr_uid_id:装饰traditional-style方法,标识将cr,uid,id作为参数
* cr_uid_id_context:装饰traditional-style方法,标识将cr,uid,id,context作为参数
* cr_uid_ids:装饰traditional-style方法,标识将cr,uid,ids作为参数
* cr_uid_ids_context:装饰traditional-style方法,标识将cr,uid,ids,context作为参数
* v7:装饰方法只支持traditional-style api,新api的方法需要重写一个新方法并用v8装饰
* v8:装饰方法只支持record-style api,旧api的方法需要重写一个新方法并用v7装饰
* constrains:返回一个指定了现实了字段限制的方法的字段依赖的装饰器,每个参数都必须是字段
* depends:返回一个指定了**compute方法**（或new style function fields)的依赖的**装饰器**，每个参数必须为以**.隔开的字段名组成的字符串**
* onchagne:返回一个对给出的fields的onchange方法的装饰器，每个参数必须为字段returns(model,downgrade=None):返回一个返回参数model的实例的方法的装饰器，参数model：model名或self(当前model),参数downgrade：要从record-style转换成traditional-style的方法

清除缓存可以使用environment对象的invalidate_all()方法进行

**@api.multi**

默认的装饰器是这个，没有自动迭代recordset，因为它默认接受的self就是recordset对象(所有recordset就是指相同模型下的所有对象，或者说同一SQL表格下的所有记录。)。

**@api.one**

@api.one装饰器将会自动产生一个迭代动作，具体是指迭代某一recordset，然后其内的self就是一个record也就是该模型下SQL表格的一条记录。然后@api.one返回的是一个列表值，某些网络客户端可能并不支持这点。所以还是尽量少用@api.one。

### 新API实例

**search** 属性

通过设置搜索参数，可以使搜索字段上的搜索。该值是返回一个方法名

实例：

```python
upper_name=fields.Char(compute=”_compute_upper” ,search='search_upper')

def search_upper(self,operation,value):   #search属性类似于XML中的search试图搜索

  if operation=='like':

  	operation='ilike'

  return [('name',operation,value)]
```

**inverses** 属性

允许在计算字段上设置值，使用该反参数。它是一个函数的名称，它将计算和设置相关字段的名称

实例：

```python
document=fields.Char(compute='compute_document',inverse=''set_document)

def compute_document(self):

  for record in self:

    with open(record.get_document_path) as f:

    record.document=f.read()

def set_document(self):

  for record in self:

    if not record.document:

    	continue

    with open(record.get_document_path()) as f:

    	f.write(record.document)
```

**related** 属性

计算字段中的一个特殊情况是关联（代理）字段，它提供的值的是关联字段的当前记录。它们通过设置相关的参数定义，像常规的计算字段，它们可以被存储。

实例：

```python
nick_name=fields.Char(related='user_id.name' ,store=True)
```

该实例中user_id字段是本表中字段与res.user模型关联，该实例直接将该user_id关联的User表数据中的 name字段值应用到本模型中，改字段存放到数据库，field类型要与user_id.name的类型一致。

**default** 属性

设置字段默认值

实例：

```python
a_field=fields.Char(default=”a value”)

b_field=fields.Char(default=compute_default_value)

def compute_default_value(self):

	return “a value”
```

### 新api之one装饰

one装饰器的作用是对**每一条记录都执行相应的方法**

应用实例：

定义columns

now=fields.Date(compute=”get_date_now”)

方法：

```python
@api.one

def get_date_now(self):

	self.date=fields.date.now()
```

### 新API之environment装饰

environment类提供了对ORM对象的封装，同时提供了对注册类的访问，记录集的缓存，以及管理重计算的数据结构。对于继承Model类来说可以直接通过self.env对environment进行操作。

属性列表：

1.user：返回当前用户

self.env.user

2.lang：返回当前语言代码

self.env.lang

3.in_draft:返回是否处于草稿状态

self.env.in_draft

4.in_onchange:返回是否处于on_change草稿模式

self.env.in_onchange

另外还有cr,registery,cache,prefetch,computed,dirty,todo,mode,all

应用说明：

1.利用env[model]获取类对象

self.env['ir.model'].search([('state','!=','manual')])

2.利用cr执行sql语句

self.env.cr.execute(query,(value,))

### 新API之Model装饰

Model装饰起的作用是**返回一个集合列表**

实例：

定义culomns

langs=fields.Selection(string='Lang', selection='get_long')

定义方法：

```python
@api.model

def get_long(self):

  langs=self.env['res.lang'].search([])

  return [(lang.code,lang.name) for lang in langs]
```

实例2：

@api.model

def some_method(self,a_value):

​	pass

等同于

old_style_model.some_method(cr,uid,a_value,context=context)

### 新API之constrains装饰

constrains用于**对字段进行限制**

实例：

定义columns

age=fields.Integer(string='Age')

定义方法：

```python
@api.constrains('age')

def __check_age(self):

	if self.age>16:

		raise ValueError(_('age must be older than 16!'))
```

### 新API之depends装饰

1. 在**计算字段值（而不是直接从数据库中读取）时使用的计算参数**。它必须将计算值分配给该字段。如果**使用其他字段的值，应该使用depends()指定这些字段**

实例：

```python
total=fields.Float(compute=“compute_total”)

@api.depends('value','tax') 

def compute_total(self):

  for record in self:

  	record.total=record.value+record.value*record.tax
 
```

2. 当使用**关联字段是可以指名路径**：

实例：

```python
@api.depends('line_ids.values')

def compute_total(self):

  for record in self:

  	record.total=sum([line.value for line in record.line_ids])
```

### 新API之onchange装饰

当**用户更改某个字段的值时（但尚未保存该表单）**，它可以自动更改基于该字段的字段值，如更改或添加一个新的发票行时，该值自动更新 

实例：

```python
@api.onchage('field1','field2')

def check_onchange(self):

  if self.field1<self.field2:

      self.field3=True
```

### 新API之multi装饰

实例：

@api.multi

def some_method(self,a_value):

​	pass

等同于

old_style_model.some_method(cr, uid, ids, a_avlue,context=context)

### 新API之returns()装饰

**返回一个对象的集合**

实例：

```python
@api.multi

@api.returns('self')

def some_method(self):

	return self

# 新的API

new_style_method=env['a.model'].browse(1,2,3)

print new_style_method.some_method()

a,model(1,2,3)

# 旧的的API

old_style_method=pool['a.model']

print old_style_method.some_method(cr,uid,[1,2,3],context=context)

[1,2,3]
```

### with_context()方法

实例：

context={key1:value1}

r1=context.with_context({},key2=value2)

\#   r1={key2:value2}

r2=context.with_context(key2=value2)

\#r2={key1:value1,key2:value2}

### 字段属性

1. default    默认——该字段的默认值；这是一个静态值，或一个函数以一个记录集和返回值
2. states     状态------字典映射状态值UI属性-值对列表；可能的属性是“只读”，“要求”，“看不见”。注：任何状态为基础的状态需要的状态字段值可在客户端的用户界面。这通常是通过包括它在相关的意见，可能是无形的，如果不相关的最终用户。
3. groups   组------逗号分隔列表（字符串），这限制了给定的组的用户的字段访问
4. copy (bool)    复制（bool）——该字段是否值应该复制记录时复制（默认：正常的字段为True，one2many未False）


