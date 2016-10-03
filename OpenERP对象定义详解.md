# OpenERP对象定义详解

**1. OpenERP对象定义的属性详细解说**
    OpenERP的对象定义的一般形式如下。
程序代码:

```python
class name_of_the_object(osv.osv):

    _name = 'xxx'

    ......

name_of_the_object()

Sample:

class qingjd(osv.osv):

    _name = 'qingjia.qingjd'

    _description = '请假单'

    _columns = {

        'shenqr': fields.many2one('hr.employee', '申请人', required=True),

    }

qingjd()
```

对象定义的完整属性如下：
必须属性
       _name     
       _columns  
可选属性
       _table  
       _description
       _defaults
       _order
       _rec_name  
       _auto  
       _constraints
       _sql_constraints
       _inherit
       _inherits

下面详细解说各个属性。
**_auto**: 是否自动创建对象对应的Table，缺省值为: True。当安装或升级模块时，OpenERP会自动在数据库中为模块中定义的每个对象创建相应的Table。当这个属性设为False时，OpenERP不会自动创建Table，这通常表示数据库表已经存在。例如，当对象是从数据库视图（View）中读取数据时，通常设为False。
**_columns**: 定义对象的字段，系统会字段为这里定义的每个字段在数据库表中创建相应的字段。关于字段（Fields）的定义，参见后文。
**_constraints**: 定义于对象上的约束（constraints），通常是定义一个检查函数，关于约束的详细说明，参见后文。
**_defaults**: 定义字段的缺省值。当创建一条新记录（record or resource）时，记录中各字段的缺省值在此定义。
**_description**: 对象说明性文字，任意文字。
**_log_access**: 是否自动在对应的数据表中增加create_uid, create_date, write_uid, write_date四个字段，缺省值为True，即字段增加。这四个字段分布记录record的创建人，创建日期，修改人，修改日期。这四个字段值可以用对象的方法（perm_read）读取。
**_name**: 对象的唯一标识符，必须是全局唯一。这个标识符用于存取对象，其格式通常是"ModuleName.ClassName",对应的，系统会字段创建数据库表"ModuleName_ClassName"。
**_order**: 定义search()和read()方法的结果记录的排序规则，和SQL语句中的order 类似，缺省值是id,即按id升序排序。详细说明参见后文。
**_rec_name**: 标识record name的字段。缺省情况（name_get没被重载的话）方法name_get()返回本字段值。_rec_name通常用于记录的显示，例如，销售订单中包含业务伙伴，当在销售订单上显示业务伙伴时，系统缺省的是显示业务伙伴记录的_rec_name。
**_sequence**: 数据库表的id字段的序列采集器，缺省值为: None。OpenERP创建数据库表时，会自动增加id字段作为主键，并自动为该表创建一个序列（名字通常是“表名_id_seq”）作为id字段值的采集器。如果想使用数据库中已有的序列器，则在此处定义序列器名。
**_sql**: _auto为True时，可以在这里定义创建数据库表的SQL语句。不过5.0以后好像不支持了，不建议使用。
**_sql_constraints**: 定义于对象上的约束（constraints），和SQL文中的约束类似，关于约束的详细说明，参见后文。
**_table**: 待创建的数据库表名，缺省值是和_name一样，只是将"."替换成"_"。
**_inherits**: 
**_inherit**: _inherits和_inherit都用于对象的继承，详细说明参见后文。


**_constraints**
    _constraints可以灵活定义OpenERP对象的约束条件，当创建或更新记录时，会触发该条件，如果条件不符合，则弹出错误信息，拒绝修改。
    _constraints的定义格式：
    [(method, 'error message', list_of_field_names), ...]

· method: 是对象的方法，该方法的格式为：def _name_of_the_method(self, cr, uid, ids): −> True|False
· error message: 不符合检查条件（method返回False）时的错误信息。
· list_of_field_names: 字段名列表，这些字段的值会出现在error message中。通常列出能帮助用户理解错误的字段。

    _constraints的例子：
程序代码: 

```python
def _constraint_sum(self, cr, uid, ids):

    cr.execute('SELECT a.currency_id

        FROM account_move m, account_move_line l, account_account a

        WHERE m.id=l.move_id AND l.account_id=a.id AND m.id IN ('+','.join(map(str, ids))+')

        GROUP BY a.currency_id')

    if len(cr.fetchall()) >= 2:

        return True

    cr.execute('SELECT abs(SUM(l.amount))

        FROM account_move m LEFT JOIN account_move_line l ON (m.id=l.move_id)

        WHERE m.id IN ('+','.join(map(str, ids))+')')

    res = cr.fetchone()[0]

    return res < 0.01

_constraints = [

    (_constraint_sum, 'Error: the sum of all amounts should be zero.', ['name'])

    ]
```

**_sql_constraints 和 _order**
    _sql_constraints定义数据表的约束条件，其格式如下例所示。
    _sql_constraints = [
        ('code_company_uniq', 'unique (code,company_id)', 'The code of the account must be unique per company !')
    ]
    本例的_sql_constraints会在数据表中增加下述约束：
    CONSTRAINT ObjectName_code_company_uniq UNIQUE(code, company_id)

    _order在对象的search或read方法中的select语句上加上"Order"子句，如 _order = 'name desc, account_id'，对应SQL文的Order子句：order by name desc, account_id。

**_defaults**
    _defaults属性用于定义字段的缺省值，其格式为：
_defaults：
    {
        'name_of_the_field':function, ...
    }

function的返回值作为'name_of_the_field'字段的缺省值。function格式是：function(obj, cr, uid, context)，返回值必须是简单类型，如boolean, integer, string 等。下面是_defaults的例子。
_defaults = {
    'date_order': lambda *a: time.strftime('%Y−%m−%d'),
    'state': lambda *a: 'draft',
    'user_id': lambda obj, cr, uid, context: uid
}

lambda是Python的行函数，"lambda obj, cr, uid, context: uid"等同于下述函数：
def func(obj, cr, uid, context):
    return uid


**_inherit和\_inherits**
    _inherit继承有两种情况，1)如果子类中不定义_name属性，则相当于在父类中增加一些字段和方法，并不创建新对象。2)如果子类中定义_name属性，则创建一个新对象，新对象拥有老对象的所有字段和方法，老对象不受任何影响。两种情况的示例及继承关系的图示见下面。
![OpenERP对象定义详解](http://shine-it.net/index.php?PHPSESSID=6778050c00297c94b5181f727f44175d&action=dlattach;topic=2159.0;attach=1086;image)
   class res_partner_add_langs(osv.osv):
       _inherit = 'res.partner'
       _columns = {
           'lang_ids' : fields.many2many('res.lang', 'res_lang_partner_rel', 'partner_id', 'lang_id', 'Languages'),
       }
   res_partner_add_langs()

![OpenERP对象定义详解(连载中...)](http://shine-it.net/index.php?PHPSESSID=6778050c00297c94b5181f727f44175d&action=dlattach;topic=2159.0;attach=1088;image)
   class formateur(osv.osv):
       _name = 'formateur'
       _inherit = 'res.partner'
       _columns = {
           'lang_ids' : fields.many2many('res.lang', 'res_lang_partner_rel', 'partner_id', 'lang_id', 'Languages'),
       }
   formateur()

    _inherits相当于多重继承。子类通过_inherits中定义的字段和各个父类关联，子类不拥有父类的字段，但可以直接操作父类的所有字段和方法。_inherits的示例及图示见下图。
![OpenERP对象定义详解(连载中...)](http://shine-it.net/index.php?PHPSESSID=6778050c00297c94b5181f727f44175d&action=dlattach;topic=2159.0;attach=1090;image)
   class cursus_category(osv.osv):
       _name = 'cursus.category'
       _inherits = {'account.analytic.caccount':'analytic_caccount_id'}
       _columns = {
           'analytic_caccount_id' : fields.many2one('account.analytic.caccount', 'ID'),
       }
   cursus_category()

**2. 一切都是对象**    

OpenERP的所有资源(Resource)都是对象，如 menus, actions, reports, invoices, partners 等等。换言之，在OpenERP中，一个菜单项，一个弹出窗口，其实都是一条数据库记录。OpenERP运行时，从数据库读出“菜单项”记录，根据该记录的信息，在屏幕上显示菜单项及其子菜单项。因此，理论上，可以不写代码，而是直接修改OpenERP的数据库而编写功能菜单、查询窗口、动作按钮等实现业务功能开发。实际开发中，通常是编写XML文件，导入菜单、窗口、动作等编程元素，实现功能开发。XML文件比直接修改数据库或编写SQL语句更容易使用一些。    

OpenERP通过自身实现的对象关系映射(ORM,object relational mapping of a database)访问数据库。OpenERP的对象名是层次结构的，就是说可以使用"."访问树状对象，如：· account.invoice : 表示财务凭证对象。· account.invoice.line : 表示财务凭证对象中的一个明细行对象。    

通常，对象名中，第一级是模块名，如: account, stock, sale 等。比之直接用SQL访问数据库，OpenERP的对象的优势有，1)直接使用对象的方法增、删、改数据库记录。因为OpenERP在基类对象中实现了常规的增、删、改方法，因而，普通对象中不需要写任何方法和代码就具备增、删、改数据库记录的功能。2)对于复杂对象，只需操作一个对象即可访问多张数据表。如partner对象，它的信息实际上存储在多张数据表中(partner address, categories, events 等等)，但只要通过"."操作即可访问所有关联表(如，partner.address.city)，简化了数据库访问。    

注意，在其他编程语言或开发平台(如Java or JavaEE)中，一个对象(Object)通常和数据库中一条记录(Record)相对应。但是，OpenERP的对象其实是一个Class，它和一个数据表(Table)对应，而不是和一个记录(Record)对应。在OpenERP中，数据库记录(Record)通常叫资源(Resource)。因为Object操作的是数据表，OpenERP的对象的方法(Method)中，几乎每个方法都带有参数ids，该参数是资源(Resource or Record)的ID（在OpenERP中ID是主键）列表，通过该ids就可以操作具体的Record了。

**3. 访问OpenERP对象**    

OpenERP提供了三种方式执行对象的方法(Method)，每种方式都是先取得对象，然后调用对象的方法。三种方式是，**1)直接使用对象，2)通过netservice使用对象，3)通过xmlrpc使用对象**。

**直接使用对象**：这种方式最简单，这种方式只能在OpenERP Server端使用，编写OpenERP的模块时候，通常使用这种方式。这个方式的内部实现原理是，OpenERP加载模块(不是安装，是启动时加载已安装模块)时，会将创建模块中的对象实例，对象实例以对象名为关键字，存储在对象池(pool)中。此方式是，从pool中取得对象，而后调用对象的方法。这个方式的一般调用形式是：    

obj=self.pool.get('name_of_the_object')    

obj.name_of_the_method(parameters_for_that_method)

第一行代码从对象池中取得对象实例，第二行代码调用对象的方法。

**Netservice方式**：这个方式和直接使用对象的方式是类似的，只是不以对象的方式呈现，而是以“服务”(Service)的方式呈现。这种方式也只能在OpenERP Server端使用，即调用程序和OpenERP Server程序在同一个Python虚拟机上运行。这个方式的内部实现原理是，类似对象池，OpenERP有一个全局变量的服务池：SERVICES，该变量位于bin\netsvc.py。有一些对象，它在创建时(\_\_init\_\_方法中)将自己提供的服务登记在服务池中，并暴露自己的服务方法(即该服务可供调用的method)。和对象池不同的是，服务可以有选择性的暴露自己的方法。OpenERP的工作流(Workflow)、报表(Report)都以服务的形式暴露自己的方法，关于OpenERP可供使用的服务有哪些，将在以后介绍。这个方式调用形式如下：    

service = netsvc.LocalService("object_proxy")    

result = service.execute(user_id, object_name, method_name, parameters)

第一行指定服务名取得服务，"object_proxy"是osv.osv对象初始化时注册的一个服务，这个服务可用于调用OpenERP的几乎所有对象(准确的说是所有从osv.osv派生的对象)。"object_proxy"服务用于调用对象的方法。第二行是其调用格式，execute是该服务暴露的一个服务方法，该方法的参数说明如下：user_id: 用户id，以用户名、密码登录后取得的id。object_name: 对象名，欲访问的对象的名称，如"res.patner"等。method_name: 方法名，欲调用的方法的名称，如"create"等。parameters: 方法的参数。

**XML−RPC方式**：这个方式相当灵活，它以HTTP协议远程访问对象，因此，能在本机、局域网、广域网范围调用OpenERP的对象的方法。该方式的调用形式是：

sock = xmlrpclib.ServerProxy('http://server_address:port_number/xmlrpc/object')

result = sock.execute(user_id, password, object_name, method_name, parameters)

参数说明如下：server_address: 运行OpenERP Server的机器的IP或域名。port_number: OpenERP Server的xmlrpc调用端口，缺省情况是8069。execute的参数和Netservice方式相同，只是多了个password参数，该参数即用户的登录密码。XML-RPC方式参考例子。这个例子以xmlrpc方式调用OpenERP的对象res.partner，在数据库中插入一条业务伙伴及其联系地址记录。因为含有中文，测试时注意代码文件保存成utf-8格式：

程序代码: 

```python
# -- encoding: utf-8 --

import xmlrpclib  #导入xmlrpc库，这个库是python的标准库。

username ='admin' #用户登录名

pwd = '123' #用户的登录密码，测试时请换成自己的密码

dbname = 'case1' #数据库帐套名，测试时请换成自己的帐套名

# 第一步，取得uid

sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')

uid = sock_common.login(dbname, username, pwd)

replace localhost with the address of the server

sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

# 调用res.partner对象的create方法在数据库中插入一个业务伙伴

partner = {

    'name': 'shine-it',

    'lang': 'zh_CN',

}

partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner)

#下面再创建业务伙伴的联系地址记录

address = {

    'partner_id': partner_id,

    'type' : 'default',

    'street': '浦东大道400号',

    'zip': '200000',

    'city': '上海市',

    'phone': '021-88888888',

}

address_id = sock.execute(dbname, uid, pwd, 'res.partner.address', 'create', address)
```

**4. 再议OpenERP的对象**

在《OpenERP应用和开发基础》的第一章中提过OpenERP的架构如下图所示：

![OpenERP对象定义详解(连载中...)](http://shine-it.net/index.php?action=dlattach;topic=2159.0;attach=1092;image)

这个架构图中，Server端的Business Object就是这里重点解说的内容。通过上面的解说，可以这样通俗的理解OpenERP的对象：每个对象就是一个代码块，包含了数据表操作(增删改查)的代码。OpenERP Server好比是一个代码池，里面装满了代码块。通过对象池、服务池、xmlrpc等方式，可以取得代码块位置(或者专业一点，叫指针)，然后调用代码块的方法，操作数据库。对象的代码什么时候装入“代码池”呢？每个对象定义的后面都有一行：name_of_the_object()，这一行实际上是创建对象实例，实例创建好以后就装到了代码池，这个装入的过程在对象的基类(osv.osv)中完成。对象的基类(osv.osv)已实现了增删改查等常规数据表操作方法，因此，只要定义好对象的字段，即使不写任何代码，该对象已经具备增删改查数据表的能力。

**5. OpenERP对象支持的字段类型**

OpenERP对象支持的字段类型有，基础类型：char, text, boolean, integer, float, date, time, datetime, binary；复杂类型：selection, function, related；关系类型：one2one, one2many, many2one, many2many。下面逐一说明。
**boolean**: 布尔型(true, false)
integer: 整数。
**float**: 浮点型，如 'rate' : fields.float('Relative Change rate',digits=(12,6)), digits定义整数部分和小数部分的位数。
**char**: 字符型，size属性定义字符串长度。
**text**: 文本型，没有长度限制。
**date**: 日期型
**datetime**: 日期时间型
**binary**: 二进制型
**function**: 函数型，该类型的字段，字段值由函数计算而得，不存储在数据表中。其定义格式为：
fields.function(fnct, arg=None, fnct_inv=None, fnct_inv_arg=None, type='float', fnct_search=None, obj=None, method=False, store=True)
· type 是函数返回值的类型。
· method 为True表示本字段的函数是对象的一个方法，为False表示是全局函数，不是对象的方法。如果method=True，obj指定method的对象。
· fcnt 是函数或方法，用于计算字段值。如果method = true, 表示fcnt是对象的方法，其格式如下：def fnct(self, cr, uid, ids, field_name, args, context)，否则，其格式如下：def fnct(cr, table, ids, field_name, args, context)。ids是系统传进来的当前存取的record id。field_name是本字段名，当一个函数用于多个函数字段类型时，本参数可区分字段。args是'arg=None'传进来的参数。
· fcnt_inv 是用于写本字段的函数或方法。如果method = true, 其格式是：def fcnt_inv(self, cr, uid, ids, field_name, field_value, args, context)，否则格式为：def fcnt_inv(cr, table, ids, field_name, field_value, args, context)
· fcnt_search 定义该字段的搜索行为。如果method = true, 其格式为：def fcnt_search(self, cr, uid, obj, field_name, args)，否则格式为：def fcnt_search(cr, uid, obj, field_name, args)
· store 表示是否希望在数据库中存储本字段值，缺省值为False。不过store还有一个增强形式，格式为 store={'object_name':(function_name,['field_name1','field_name2'],priority)} ，其含义是，如果对象'object_name'的字段['field_name1','field_name2']发生任何改变，系统将调用函数function_name，函数的返回结果将作为参数(arg)传送给本字段的主函数，即fnct。

**selection**: 下拉框字段。定义一个下拉框，允许用户选择值。如：'state': fields.selection((('n','Unconfirmed'),('c','Confirmed')),'State', required=True)，这表示state字段有两个选项('n','Unconfirmed')和('c','Confirmed')。

**one2one**: 一对一关系，格式为：fields.one2one(关联对象Name, 字段显示名, ... )。在V5.0以后的版本中不建议使用，而是用many2one替代。
**many2one**: 多对一关系，格式为：fields.many2one(关联对象Name, 字段显示名, ... )。可选参数有：ondelete，可选值为"cascade"和"null"，缺省值为"null"，表示one端的record被删除后，many端的record是否级联删除。

**one2many**: 一对多关系，格式为：fields.one2many(关联对象Name, 关联字段, 字段显示名, ... ),例：'address': fields.one2many('res.partner.address', 'partner_id', 'Contacts')。

**many2many**: 多对多关系。例如：
    'category_id':fields.many2many('res.partner.category','res_partner_category_rel','partner_id','category_id','Categories'),
表示以多对多关系关联到对象res.partner.category，关联表为'res_partner_category_rel'，关联字段为'partner_id'和'category_id'。当定义上述字段时，OpenERP会自动创建关联表为'res_partner_category_rel'，它含有关联字段'partner_id'和'category_id'。

**reference**: 引用型，格式为：fields.reference(字段名, selection, size, ... )。其中selection是: 1)返回tuple列表的函数，或者 2)表征该字段引用哪个对象(or model)的tuples列表。reference字段在数据库表中的存储形式是（对象名，ID），如(product.product,3)表示引用对象product.product（数据表product_product）中id=3的数据。reference的例子：
    def _links_get(self, cr, uid):
        cr.execute('select object,name from res_request_link order by priority')
        return cr.fetchall()

    ...
    'ref':fields.reference('Document Ref 2', selection=_links_get, size=128),
    ...
上例表示，字段ref可以引用哪些对象类型的resource，可引用的对象类型从下拉框选择。下拉框的选项由函数_links_get返回，是(object,name)对的列表，如[("product.product","Product"), ("account.invoice","Invoice"), ("stock.production.lot","Production Lot")] 。

**related**: 关联字段，表示本字段引用关联表中的某字段。格式为：fields.related(关系字段,引用字段,type, relation, string, ...)，关系字段是本对象的某字段（通常是one2many or many2many），引用字段是通过关系字段关联的数据表的字段，type是引用字段的类型，如果type是many2one or many2many, relation指明关联表。例子如下：
        'address': fields.one2many('res.partner.address', 'partner_id', 'Contacts'),
        'city':fields.related('address','city',type='char', string='City'),
        'country':fields.related('address','country_id',type='many2one', relation='res.country', string='Country'),

这里，city引用address的city字段，country引用address的country对象。在address的关联对象res.partner.address中，country_id是many2one类型的字段，所以type='many2one', relation='res.country'。

**property**: 属性字段，下面以具体例子解说property字段类型。
'property_product_pricelist': fields.property('product.pricelist', type='many2one', relation='product.pricelist',string="Sale Pricelist", method=True, view_load=True, group_name="Pricelists Properties")
这个例子表示，本对象通过字段'property_product_pricelist'多对一(type='many2one')关联到对象product.pricelist(relation='product.pricelist')。和many2one字段类型不同的是，many2one字段会在本对象中创建数据表字段'property_product_pricelist'，property字段类型不会创建数据表字段'property_product_pricelist'。property字段类型会从数据表ir.property中查找name='property_product_pricelist'(即字段定义中的'product.pricelist'加上前缀property，并将"."替换成"_"作为name)且company_id和本对象相同的记录，从该记录的value字段(value字段类型为reference)查得关联记录，如(product.pricelist,1)，表示本对象的resource多对一关联到对象product.pricelist的id=1的记录。也就是说，property字段类型通过ir.property间接多对一关联到别的对象。
    property字段类型基本上和many2one字段类型相同，但是有两种情况优于many2one字段。其一是，例如，当有多条记录通过ir.property的name='property_product_pricelist'的记录关联到记录(product.pricelist,1)，此时，如果希望将所有关联关系都改成关联到记录(product.pricelist,2)。如果是many2one类型，不写代码，很难完成此任务，是property字段的话，只要将ir.property中的value值(product.pricelist,1)改成(product.pricelist,2)，则所有关联关系都变了。修改ir.property的value值可以在系统管理下的菜单Configuration --> Properties中修改。其二是，例如，同一业务伙伴，但希望A公司的用户进来看到的该业务伙伴价格表为pricelistA，B公司的用户进来看到的该业务伙伴价格表为pricelistB，则many2one类型达不到该效果。property类型通过ir.property中的记录关联时加上了company_id的条件，因此可以使得不同公司的员工进来看到不同的关联记录。
    由于property类型通过ir.property关联，因此，每个property类型的字段都必须在ir.property中有一条关联记录。这可以在安装时导入该条记录，参考代码如下：
    <record model="ir.property" id="property_product_pricelist">
        <field name="name">property_product_pricelist</field>
        <field name="fields_id" search="[('model','=','res.partner'), ('name','=','property_product_pricelist')]"/>
        <field name="value" eval="'product.pricelist,'+str(list0)"/>
    </record>

**6. 字段定义的参数**
    字段定义中可用的参数有， change_default，readonly，required，states，string，translate，size，priority，domain，invisible，context，selection。
**change_default**：别的字段的缺省值是否可依赖于本字段，缺省值为：False。例子(参见res.partner.address)，
    'zip': fields.char('Zip', change_default=True, size=24),

这个例子中，可以根据zip的值设定其它字段的缺省值，例如，可以通过程序代码，如果zip为200000则city设为“上海”，如果zip为100000则city为“北京”。

**readonly**: 本字段是否只读，缺省值：False。
**required**: 本字段是否必须的，缺省值：False。
**states**: 定义特定state才生效的属性，格式为：{'name_of_the_state': list_of_attributes}，其中list_of_attributes是形如[('name_of_attribute', value), ...]的tuples列表。例子(参见account.transfer)：
    'partner_id': fields.many2one('res.partner', 'Partner', states={'posted':[('readonly',True)]}),

**string**: 字段显示名，任意字符串。
**translate**: 本字段值（不是字段的显示名）是否可翻译，缺省值：False。
**size**: 字段长度。
**priority**: 
**domain**: 域条件，缺省值：[]。在many2many和many2one类型中，字段值是关联表的id，域条件用于过滤关联表的record。例子：
'default_credit_account_id': fields.many2one('account.account', 'Default Credit Account', domain="[('type','!=','view')]"),

本例表示，本字段关联到对象('account.account')中的，type不是'view'的record。

**invisible**: 本字段是否可见，即是否在界面上显示本字段，缺省值True。
**selection**: 只用于reference字段类型，参见前文reference的说明。

**7. OpenERP对象的预定义方法**

每个OpenERP的对象都有一些预定义方法，这些方法定义在基类osv.osv中。这些预定义方法有:
**基本方法**：create, search, read, browse, write, unlink。
    def create(self, cr, uid, vals, context={})
    def search(self, cr, uid, args, offset=0, limit=2000)
   def read(self, cr, uid, ids, fields=None, context={})
   def browse(self, cr, uid, select, offset=0, limit=2000)
   def write(self, cr, uid, ids, vals, context={})
   def unlink(self, cr, uid, ids)

**缺省值存取方法**：default_get, default_set。
def default_get(self, cr, uid, fields, form=None, reference=None)
def default_set(self, cr, uid, field, value, for_user=False)

**特殊字段操作方法**：perm_read, perm_write
def perm_read(self, cr, uid, ids)
def perm_write(self, cr, uid, ids, fields)

**字段(fields)和视图(views)操作方法**：fields_get, distinct_field_get, fields_view_get
def fields_get(self, cr, uid, fields = None, context={})
def fields_view_get(self, cr, uid, view_id=None, view_type='form',context={})
def distinct_field_get(self, cr, uid, field, value, args=[], offset=0,limit=2000)

**记录名字存取方法**：name_get, name_search
def name_get(self, cr, uid, ids, context={})
def name_search(self, cr, uid, name='', args=[], operator='ilike',context={})

**缺省值存取方法**：default_get, default_set
def name_get(self, cr, uid, ids, context={})
def name_search(self, cr, uid, name=, args=[], operator=’ilike’, context={})

**create**方法：在数据表中插入一条记录（或曰新建一个对象的resource）。
格式：def create(self, cr, uid, vals, context={})
参数说明：
vals: 待新建记录的字段值，是一个字典，形如: {'name_of_the_field':value, ...}
context (optional): OpenERP几乎所有的方法都带有参数context，context是一个字典，存放一些上下文值，例如当前用户的信息，包括语言、角色等。context可以塞入任何值，在action定义中，有一个context属性，在界面定义时，可以在该属性中放入任何值，context的最初值通常来自该属性值。
返回值：新建记录的id。
举例：id = pooler.get_pool(cr.dbname).get('res.partner.event').create(cr, uid,{'name': 'Email sent through mass mailing','partner_id': partner.id,'description': 'The Description for Partner Event'})

**search**方法：查询符合条件的记录。
格式：def search(self, cr, uid, args, offset=0, limit=2000)
参数说明：
args: 包含检索条件的tuples列表，格式为: [('name_of_the_field', 'operator', value), ...]。可用的operators有：
  =, >, <, <=, >=
  in
  like, ilike
  child_of
更详细说明，参考《OpenERP应用和开发基础》中的“域条件”有关章节。

· offset (optional): 偏移记录数，表示不返回检索结果的前offset条。
· limit (optional): 返回结果的最大记录数。
返回值：符合条件的记录的id list。

**read**方法：返回记录的指定字段值列表。
格式：def read(self, cr, uid, ids, fields=None, context={})
参数说明：
· ids: 待读取的记录的id列表，形如[1,3,5,...]
· fields (optionnal): 待读取的字段值，不指定的话，读取所有字段。
· context (optional): 参见create方法。
返回值：返回读取结果的字典列表，形如 [{'name_of_the_field': value, ...}, ...]

**browse**方法：浏览对象及其关联对象。从数据库中读取指定的记录，并生成对象返回。和read等方法不同，本方法不是返回简单的记录，而是返回对象。返回的对象可以直接使用"."存取对象的字段和方法，形如"object.name_of_the_field"，关联字段(many2one等)，也可以通过关联字段直接访问“相邻”对象。例如：
    addr_obj = self.pool.get('res.partner.address').browse(cr, uid, contact_id)
    nom = addr_obj.name
    compte = addr_obj.partner_id.bank
这段代码先从对象池中取得对象res.partner.address，调用它的方法browse，取得id=contact_id的对象，然后直接用"."取得"name"字段以及关联对象patner的银行(addr_obj.partner_id.bank)。

格式：def browse(self, cr, uid, select, offset=0, limit=2000)
参数说明：
select: 待返回的对象id，可以是一个id，也可以是一个id 列表。
· offset (optional): 参见search方法。
· limit (optional): 参见search方法。
返回值：返回对象或对象列表。
注意：本方法只能在Server上使用，由于效率等原因，不支持rpc等远程调用。

**write**方法：保存一个或几个记录的一个或几个字段。
格式：def write(self, cr, uid, ids, vals, context={})
参数说明：
· ids: 待修改的记录的id列表。
· vals: 待保存的字段新值，是一个字典，形如: {'name_of_the_field': value, ...}。
· context (optional): 参见create方法。
返回值：如果没有异常，返回True，否则抛出异常。
举例：self.pool.get('sale.order').write(cr, uid, ids, {'state':'cancel'})

**unlink**方法：删除一个或几个记录。
格式：def unlink(self, cr, uid, ids)
参数说明：
· ids: 待删除的记录的id列表。
返回值：如果没有异常，返回True，否则抛出异常。


**default_get**方法：复位一个或多个字段的缺省值。
格式: def default_get(self, cr, uid, fields, form=None, reference=None)
参数说明:
• fields: 希望复位缺省值的字段列表。
• form (optional): 目前似乎未用(5.06版)。
• reference (optional): 目前似乎未用(5.06版)。
返回值: 字段缺省值，是一个字典，形如： {'field_name': value, ... }。
举例：self.pool.get('hr.analytic.timesheet').default_get(cr, uid, ['product_id','product_uom_id'])

**default_set**方法：重置字段的缺省值。
格式: def default_set(self, cr, uid, field, value, for_user=False)
参数说明:
• field: 待修改缺省值的字段。
• value: 新的缺省值。
• for_user (optional): 修改是否只对当前用户有效，还是对所有用户有效，缺省值是对所有用户有效。
返回值: True