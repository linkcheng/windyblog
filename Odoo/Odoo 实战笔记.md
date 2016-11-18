# Odoo 笔记

1. i18n 书写格式：
```
#. module: hr_base
#: model:ir.actions.act_window,name:hr_base.action_bank_type_view
#: model:ir.model,name:hr_base.model_bank_identification_number_type
#: model:ir.model.fields,field_description:hr_base.field_bank_account_information_bank_identification_number_type
#: model:ir.ui.menu,name:hr_base.bank_identification_number_type_menu
#: model:ir.ui.view,arch_db:hr_base.bank_identification_number_type_view_form
#: model:ir.ui.view,arch_db:hr_base.bank_identification_number_type_view_tree
msgid "Bank Identification Number Type"
msgstr "金融机构识别码类型"
```
2. One2many:会默认对应tree视图，即使不自己写

3. 初始化数据，通常是在 data/ 目录下，通过 xml 或者 json文件的方式。xml 中通过方式添加。noupdate="1"。

   ```
   <data noupdate="1">
     <record id="bank_identification_number_type_001" model="bank.identification.number.type">
       <field name="no">1</field>
       <field name="name">ABA Number</field>
     </record>
   </data>
   ```

4. 修改 model 中的字段，当一个 model 在多处有被继承扩展时，字段只发生**位置变更**而不发生**名称变更**，则在数据库中不会有字段变化。

5. 当在一个 model 中没有定义 name字段时，可以用 **_rec_name** 来制定一个字段来行使 name 字段作用。

6. 跟新数据库：orm 与 直接运行 sql 语句

   ```
   if partner_record:
     partner_record[0].sudo().write(partner_val)
     # partner_id = config.execute_sql_operation('sql_update_dict', 'res_partner', record_dict=partner_val, record_id=partner_val['id'])
   else:
     partner_id = config.execute_sql_operation('sql_insert_dict', 'res_partner', record_dict=partner_val)
     # env['company.record'].sudo().create(company_record_dict)
   ```

7. 通过 sql 语句查询数据库返回结果：

   ```
   self._cr.execute(select_sql, value_list)
   return self._cr.dictfetchall()  # 返回 list(dict)
   # return self._cr.fetchall()  # 返回 list(tuple)
   ```

8. 一个python脚本，本来都运行好好的，然后写了几行代码，而且也都确保每行都对齐了，但是运行的时候，却出现语法错误： 
   IndentationError: unindent does not match any outer indentation level

   【解决过程】 
   1.对于此错误，最常见的原因是，的确没有对齐。但是我根据错误提示的行数，去代码中看了下，没啥问题啊。 
   都是用TAB键，对齐好了的，没有不对齐的行数啊。 
   2.以为是前面的注释的内容影响后面的语句的语法了，所以把前面的注释也删除了。 
   结果还是此语法错误。 
   3.把当前python脚本的所有字符都显示出来看看有没有啥特殊的字符。

9. 设置显示状态

   ```xml
   <field name="model_id" domain="[('transient','=', False)]" options="{'no_create': True, 'no_open': True}"/>                               
   <notebook attrs="{'invisible': [('model_id','=', False)]}">
   ```

10. 使用logging模块记录后台行为日志

```python
   import logging 
   _logger = logging.getLogger(__name__) 
   … 
   _logger.warning('Validate Error!') 
```

11. 删除约束关系 ： 

```sql
   ALTER TABLE "import_fields" DROP CONSTRAINT "import_fields_import_field_id_unique";
```

12.    数据库查询 select语句：SELECT  * from table_name where id='id';

13.    修改数据：

       ```sql
                         UPDATE ir_translation SET value='员工标签' WHERE lang='zh_CN' and src='Categories' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='category_ids' and model='hr.employee');
       ```

14.    数据库左连接查询：

       ```sql
                         """ SELECT fol.id,fol.res_model,fol.res_id FROM mail_followers fol LEFT JOIN mail_followers_mail_message_subtype_rel rel ON fol.id=rel.mail_followers_id WHERE rel.mail_message_subtype_id=%s AND fol.active=TRUE AND fol.partner_id=%s AND fol.write_date <= %s""" % (attention_id, partner_id, deadline_date)
       ```

15.    write 方法重写：

       ```python
                   @api.one
                   def write(self, val):
                       result = super(all_form_design_menu, self).write(val)
                       if self.menu_id:
                           menu_var = self.env['ir.ui.menu'].browse(self.menu_id.id)
                           menu_var.write({'name': self.name})
                           return result
       ```

16.    添加 function tool，在 debug 模式下，添加 function tool item，model 为 all.form.design，类型为 method，方法名称为：add_state_change_date_field

       ```python
                   @api.model
                   def add_state_change_date_field(self):
                       # 用来处理旧的e表单数据没有x_state_change_date字段的问题；需要添加列也需要添加字段
                       form_design_objs = self.env['all.form.design'].search([])
                       for form_design_obj in form_design_objs:
                           has_state_change_date = filter(lambda x: x.name in ['x_state_change_date'], 					form_design_obj.ir_model_id.field_id)
                           if not has_state_change_date:
                               query = 'alter table %s add x_state_change_date date;' % 										form_design_obj.ir_model_id.model
                               self._cr.execute(query)
                               vals = {
                                   'model': form_design_obj.ir_model_id.model,
                                   'model_id': form_design_obj.ir_model_id.id,
                                   'name': 'x_state_change_date',
                                   'ttype': 'date',
                                   'field_description': _('Date of state change'),
                               }
                               self.env['ir.model.fields'].create(vals)
       ```

       ```xml
                   <?xml version="1.0" encoding="UTF-8"?>
                   <openerp>
                     <data noupdate="1">
                       <record id="all_form_design_func" model="function_tool">
                         <field name="model">all.form.design</field>
                         <field name="table">all_form_design</field>
                         <field name="method">add_state_change_date_field</field>
                         <field name="type">method</field>
                       </record>
                     </data>
                   </openerp>
       ```

17.    旧API接口调用新API接口函数，需要补齐 **cr, uid, context=None** 三个参数

18.    self.ensure_one()

       ```python
                   """checks that the recordset is a singleton (only contains a single record), raises an error otherwise:"""
                   records.ensure_one()
                   # is equivalent to but clearer than:
                   assert len(records) == 1, "Expected singleton"
       ```

19.    确保入参是 list 类型

       ```python
                   if isinstance(ids, (int,long)): 
                       ids = [ids]
       ```

20.    Odoo 对象成员赋值 （=）时会调用 write 方法，可以通过中间变量代替：

       ```python
                   instance = self.env[attention['res_model']].browse(attention['res_id'])
                   # instance.state_change_date = instance.write_date ， 修改为以下代码
                   instance_state_change_date = instance.state_change_date
                   if not instance_state_change_date:
                       instance_state_change_date = instance.write_date
       ```

21.    手动调用 query = 'alter table x_fx__2016_0015 add x_state_change_date date;' 与 self.env['ir.model.fields'].create(vals) 方式添加一列与一个字段，列名称（字段名称）必须以 **x_** 开头。

22.    翻译问题，比如动态model名称，_(‘Description’) 类型，可以通过导出po文件查看，然后进行修改。_() 函数会调用po文件所对应的翻译。

       ```po
                   #. module: all_form_design
                   #: code:addons/all_form_design/all_form_design.py:1765
                   #, python-format
                   msgid "Date of state change"
                   msgstr "状态变更日期"
       ```

23.    xml 继承拓展问题：

       ```xml
                   <record id="view_form_department_inherited" model="ir.ui.view">
                     <field name="name">Hr department inherited Form</field>
                     <field name="model">hr.department</field>
                     <field name="inherit_id" ref="hr_base.view_department_form"/>
                     <!-- ref 表示要扩招的xml record_id -->
                     <field name="arch" type="xml">
                       <field name="company_id" position="after">
                       <!-- name 表示要扩招的xml field_id, position 表示下边的field所要添加的位置 -->
                         <field name="department_color" />
                       </field>
                     </field>
                   </record>
       ```

24.    取today的方法

       1.    ```
             from openerp import fields
             from openerp.fields import Date
             today = fields.date.context_today(self, cr, uid, context=context) # 旧API，# (日期时间)
             today = Date.from_string(Date.today())
             ```

       2.    ```
                                     from datetime import date
                                     today = date.today()
             ```

             3.    ```
                   import datetime
                   today = datetime.datetime.strptime(fields.Date.context_today(self), '%Y-%m-%d')
                   today = datetime.datetime.today().strftime("%Y-%m-%d")

                   now_time = datetime.datetime.now()  # (only日期)
                   now_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
                   today = now_time.strftime('%Y-%m-%d')
                   ```

             4.    ```
                               yesterday = (datetime.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
                               tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
                   ```

25.    定时任务

                   ```
                   <!--定时任务-->
                   <record forcecreate="True" id="ir_cron_update_expired" model="ir.cron">
                       <field name="name">更新组织单元是否过期</field>
                       <field name="active" eval="True"/>
                       <field name="user_id" ref="base.user_root"/>
                       <field name="interval_number">1</field>
                       <field name="interval_type">days</field>
                       <field name="nextcall">2000-01-01 00:00:00</field>
                       <field name="numbercall">-1</field>
                       <field name="doall" eval="True"/>
                       <field name="model" eval="'hr.department'"/>
                       <field name="function" eval="'update_expired'"/>
                   </record>
                   ```

26.    **_search()** 方法，所有 search(), name_search(), 最后到会调用 **_search()** 方法，以下是重写**_search()** 的一个示例：（search(), 为通过过滤器，action_widonw 加载时调用的； name_search() 是作为 many2one 字段时调用的）

                ```
                @api.model
                def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
                    args = args or []
              
                    active, is_expired = False, False
                    for domain in args:
                        if 'active' in domain:
                            active = True
                        if 'is_expired' in domain:
                            is_expired = True
              
                    extra_domain = []
                    if not active:
                        extra_domain.append(('active', '=', True))
                    if not is_expired:
                        extra_domain.append(('is_expired', '=', False))
              
                    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
                    extra_domain.append(('start_date', '<', tomorrow))
              
                    args = extra_domain + args
              
                    return super(HrDepartment, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
                ```

27.    sql 递归查询

```sql
SELECT emp.id, emp.name, dep.id as department_id, dep.name as department_name, 
  dep.parent_id as parent_department,dep.manager_id as manager_id, 
  dep.now_num as department_number,col.color_code as color,
  emp.image_small_url as image_url,emp.job_id,job.name as job_name,
  emp.manager,emp.work_phone,emp.work_email,emp.employee_number
FROM hr_department dep
  LEFT JOIN hr_employee emp on emp.id=dep.manager_id
  LEFT JOIN display_color col on dep.department_color=col.id
  LEFT JOIN hr_job job on emp.job_id=job.id
WHERE dep.id IN
  (WITH RECURSIVE r AS (
    SELECT * FROM hr_department WHERE id=81
    UNION ALL
    SELECT hr_department.* FROM hr_department, r WHERE hr_department.parent_id = r.id AND
    hr_department.is_in_use=True
    )
  SELECT id FROM r ORDER BY id);
```

> WITH RECURSIVE 是递归查询

第一步  SELECT * FROM hr_department WHERE id=81 ，并放在 r 中。

第二步  SELECT hr_department.* FROM hr_department, r WHERE hr_department.parent_id = r.id AND
​    hr_department.is_in_use=True   放入 r 中。 

第三步 不断循环第二步，直到遍历 hr_department 所有记录。

第四步 UNION ALL。取 1 2 3 步 并集，保留重复记录。

> LEFT JOIN 是左连接；

LEFT JOIN 关键字会从左表 (hr_department) 那里返回所有的行，即使在右表 (hr_employee) 中没有匹配的行。在某些数据库中， LEFT JOIN 称为 LEFT OUTER JOIN。

28. function 字段

```python
def _get_department_num(self, cr, uid, ids, name, args, context=None):
    res = {}
    for id in ids:
        department_ids = self.search(cr, SUPERUSER_ID, [('parent_id', 'child_of', id)])
        employee_num = self.pool.get('hr.employee').search_count(cr, SUPERUSER_ID, [('department_id', 'in', department_ids), ('work_activity', '=', 'in_service')])
        res[id] = employee_num
        return res

def _get_all_department_ids(self, cr, uid, ids, context=None):
    # 一个员工部门发生变化时，重新计算所有部门的员工数
    # 一个部门name发生变化时，重新计算所有部门的display_name
    return self.pool.get('hr.department').search(cr, SUPERUSER_ID, [])

'now_num': fields.function(_get_department_num, string="No. of Employee", store={
    'hr.employee': (_get_all_department_ids, ['department_id', 'active', 'work_activity'], 10),
    'hr.department': (_get_all_department_ids, ['name', 'parent_id'], 10),
}, type='integer'),
```

> 当 'hr.employee' 的 'department_id', 'active', 'work_activity' 字段发生变化时，触发**_get_all_department_ids** 函数，发返回值返回给 **_get_department_num** 作为参数，此处返回 ids。

29. @api.onchange() 说明

```python
@api.onchange('end_date')
def on_change_end_date(self):
    '''
        当 end_date 变更时调用
        :param end_date: 组织单元有效期止
        :param now_num: 组织单元下员工数
        :return: 如果 end_date 设置为未来的一个定值，并且该组织单元下有员工，raise warning，
        '''

    today = datetime.now().strftime('%Y-%m-%d')
    if self.end_date and self.end_date > today:
        if self.now_num != 0:
            raise osv.except_osv(_('Warning'), _('There are employees assigned to this org unit ,please adjust before the org unit gets expired.'))

     # return {'domain': {'child_source_id': [('partner_parent_id', '=', self.source_id.id)]},}
```

> @api.onchange 装饰的函数通常没有返回值，如果有应该为 {‘domain’：{}}
>
> on_change_end_date 的参数应该只为 self

30. 新 API compute 

```python
@api.depends('start_date', 'end_date')
    def _compute_is_in_use(self):
        '''
        根据 start_date end_date 计算 is_in_use
        :return:
        '''
        for department in self:
        	department.is_in_use = department.is_department_in_use(department.start_date, department.end_date)

    # is_in_use 表示是否在使用，根据 today 是否在 [start_date, end_date] 中而得，in，为 True， 否则 False
is_in_use = fields_new.Boolean('In Use', compute='_compute_is_in_use', store=True)
```

```python
# 关注者和待办者,如果是方法则调方法,如果是某个字段那就直接拿字段
field_value = model_search_rule[field](self) if callable(model_search_rule[field]) else model_search_rule[field]
```

31.  新旧 api 比较

    新 api ：


```python
departments = self.env['hr.department'].search([('active', '=', True)])  # 对象列表
ir_values = self.env['ir.values'].browse(ir_values_id)  # 对象列表
```

​	旧 api：

```python
ids = self.search(cr, uid, [('name', '=', name)], context=context)  # id 列表
employees = self.browse(cr, uid, ids, context=context)  # 对象列表
```

32. 新 api 中 self，self 为 recordset

```python
 @api.depends('start_date', 'end_date')
 def _compute_is_in_use(self):
    '''
        根据 start_date end_date 计算 is_in_use
        :return:
        '''
    for department in self:
        department.is_in_use = department.is_department_in_use(department.start_date, department.end_date)

```

33. workflow_ 开头的函数，context 为空，如 

```python
def workflow_done(self, cr, uid, ids, context=None):
    pass
```

34. 查询组织单元，并且找对应翻译

```python
@api.model
def get_department_structure(self, department_ids, employee_ids):
    sql = """SELECT id, name, parent_id, manager_id FROM hr_department WHERE id IN (
                   WITH RECURSIVE r AS (
                        SELECT * FROM hr_department WHERE id = ANY(%s)
                        UNION ALL
                        SELECT hr_department.* FROM hr_department, r WHERE hr_department.parent_id=r.id  AND hr_department.active=True AND hr_department.is_in_use=True
                    )
                    SELECT id FROM r ORDER BY id
                );"""

    self.env.cr.execute(sql, (department_ids.ids,))
    departments = self.env.cr.fetchall()

    self._cr.execute(
        "select src,value from ir_translation where lang='%s' and name='%s'" % (self._context['lang'], 'hr.department,name'))
    dep_lists = self._cr.fetchall()
    dep_dic = {}
    for dep in dep_lists:
        dep_dic[dep[0]] = dep[1]

        def set_dep(dep, dep_dic):
            temp = list(dep)
            temp.__setitem__(1, dep_dic.get(dep[1], dep[1]))
            dep = tuple(temp)
            return dep

        departments = [set_dep(dep, dep_dic) for dep in departments]
        self.env.cr.execute(
            "select	 hr_employee.id,hr_employee.name,hr_employee.department_id,hr_employee.parent_id,work_phone,gender,work_email,birthday,work_location,image_small_url,res_users.id,res_users.rong_uid,hr_employee.notes,hr_job.name from hr_employee, res_users, hr_job where hr_employee.user_id=res_users.id and hr_employee.job_id=hr_job.id and hr_employee.id = ANY(%s);",
            (employee_ids.ids,))
        employees = self.env.cr.fetchall()
        org_tree = org_structure.Org_StructureTree()
        org_tree.init_Org_Tree(departments, employees)
        org_dict = org_tree.get_Org_Structure()
        return org_dict	
```

```python
    @api.model
    def get_specify_field_translations(self, name, field_type, lang):
        """
        根据 ir_translation 的 name 和 field_type 查找对应的原文和译文
        :param name: ir.translation name
        :param field_type: 条目类型
        :param lang: 语言
        :return: 原文-译文 组成的 key-value 字典
        """
        # 按id升序排列，确保最新id在字典中为有效翻译
        query = """ SELECT src,value FROM ir_translation WHERE lang=%s AND type=%s AND name=%s ORDER BY id"""
        params = (lang, field_type, name)
        self.env.cr.execute(query, params)
        menu_trans = self.env.cr.fetchall()
        return {rec[0]: rec[1] for rec in menu_trans}
```

