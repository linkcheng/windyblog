# Odoo中的字段类型

Odoo对象支持的字段类型有:

基础类型：char, text, boolean, integer, float, date, time, datetime, binary；

复杂类型：selection, function, related；

关系类型：one2one, one2many, many2one, many2many。



char: 字符型，size属性定义字符串长度。

text: 文本型，没有长度限制。

boolean: 布尔型(true, false)

integer: 整数

float: 浮点型，如 'rate' : fields.float('Relative Change rate',digits=(12,6)), digits定义整数部分和小数部分的位数，在odoo中如果不添加digits属性默认保留2位小数。

date: 日期型

datetime: 日期时间型

binary: 二进制型

 

function: 函数型，该类型的字段，字段值由函数计算而得，不存储在数据表中。其定义格式为：

fields.function(fnct, arg=None, fnct_inv=None, fnct_inv_arg=None, type='float', fnct_search=None, obj=None, method=False, store=True)

* type 是函数返回值的类型。
* method 为True表示本字段的函数是对象的一个方法，为False表示是全局函数，不是对象的方法。如果method=True，obj指定method的对象。
* fcnt 是函数或方法，用于计算字段值。如果method = true, 表示fcnt是对象的方法，其格式如下：def fnct(self, cr, uid, ids, field_name, args, context)，否则，其格式如下：def fnct(cr, table, ids, field_name, args, context)。ids是系统传进来的当前存取的record id。field_name是本字段名，当一个函数用于多个函数字段类型时，本参数可区分字段。args是'arg=None'传进来的参数。
* fcnt_inv 是用于写本字段的函数或方法。如果method = true, 其格式是：def fcnt_inv(self, cr, uid, ids, field_name, field_value, args, context)，否则格式为：def fcnt_inv(cr, table, ids, field_name, field_value, args, context)
* fcnt_search 定义该字段的搜索行为。如果method = true, 其格式为：def fcnt_search(self, cr, uid, obj, field_name, args)，否则格式为：def fcnt_search(cr, uid, obj, field_name, args)
* store 表示是否希望在数据库中存储本字段值，缺省值为False。不过store还有一个增强形式，格式为 store={'object_name':(function_name,['field_name1','field_name2'],priority)} ，其含义是，如果对象'object_name'的字段['field_name1','field_name2']发生任何改变，系统将调用函数function_name，函数的返回结果将作为参数(arg)传送给本字段的主函数，即fnct。

 

selection: 下拉框字段。定义一个下拉框，允许用户选择值。如：'state': fields.selection((('n','Unconfirmed'),('c','Confirmed')),'State', required=True)，这表示state字段有两个选项('n','Unconfirmed')和('c','Confirmed')。

 

one2one: 一对一关系，格式为：fields.one2one(关联对象Name, 字段显示名, ... )。在V5.0以后的版本中不建议使用，而是用many2one替代。

many2one: 多对一关系，格式为：fields.many2one(关联对象Name, 字段显示名, ... )。可选参数有：ondelete，可选值为"cascade"和"null"，缺省值为"null"，表示one端的record被删除后，many端的record是否级联删除。

one2many: 一对多关系，格式为：fields.one2many(关联对象Name, 关联字段, 字段显示名, ... ),例：'address': fields.one2many('res.partner.address', 'partner_id', 'Contacts')。

many2many: 多对多关系。例如：

 'category_id':fields.many2many('res.partner.category','res_partner_category_rel','partner_id','category_id','Categories'),

表示以多对多关系关联到对象res.partner.category，关联表为'res_partner_category_rel'，关联字段为'partner_id'和'category_id'。当定义上述字段时，OpenERP会自动创建关联表为'res_partner_category_rel'，它含有关联字段'partner_id'和'category_id'。'res_partner_category_rel' 在odoo中未创建模型，所以只能通过sql访问。