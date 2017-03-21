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

#. module: employee_dimission
#: selection:employee.dimission,state:0
#: selection:hr.dimission,state:0
msgid "Draft"
msgstr "草稿"

#. module: hr_rank_job_transfer
#: model:ir.ui.view,arch_db:hr_rank_job_transfer.report_rank_job_transfer
msgid "<span>Effective Date</span>"
msgstr "<span>生效日期</span>"

#. module: hr_rank_job_transfer
#: model:ir.actions.act_window,name:hr_rank_job_transfer.action_rank_job_transfer_view
#: model:ir.actions.report.xml,name:hr_rank_job_transfer.action_report_rank_job_transfer
#: model:ir.ui.menu,name:hr_rank_job_transfer.menu_rank_job_transfer
#: model:ir.model,name:hr_rank_job_transfer.model_rank_job_transfer
#: model:ir.ui.view,arch_db:hr_rank_job_transfer.rank_job_transfer_form_view
#: model:ir.ui.view,arch_db:hr_rank_job_transfer.rank_job_transfer_tree_view
msgid "Organizational Adjustment"
msgstr "岗位职级调整"

#. module: hr_base
#: model:ir.model,name:hr_base.model_employee_birthday_wish_config  ; model 名称
#: model:ir.actions.act_window,name:hr_base.action_employee_birthday_wish_config  
; action ，model="ir.actions.act_window"
#: model:ir.ui.menu,name:hr_base.menu_employee_birthday_wish_config ; 菜单
#: model:ir.ui.view,arch_db:hr_base.employee_birthday_wish_config_form_view  ; 视图
msgid "Employee Birthday Wishes Config"
msgstr "员工生日祝福"

#. module: hr_base
#: code:addons/hr_base/hr_base_models.py:32
#: sql_constraint:unit.type:0  # sql提示语句翻译
#, python-format
msgid "Org unit type code repeat !"
msgstr "编码重复！"
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

   ```python
   if partner_record:
     partner_record[0].sudo().write(partner_val)
     # partner_id = config.execute_sql_operation('sql_update_dict', 'res_partner', 		    	record_dict=partner_val, record_id=partner_val['id'])
   else:
     partner_id = config.execute_sql_operation('sql_insert_dict', 'res_partner', 					record_dict=partner_val)
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

13. 修改数据：

  ```sql
  UPDATE ir_translation SET value='员工标签' WHERE lang='zh_CN' and src='Categories' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='category_ids' and model='hr.employee');
  ```
  ```

  ```

14. 数据库左连接查询：

  ```sql
  """ SELECT fol.id,fol.res_model,fol.res_id FROM mail_followers fol LEFT JOIN mail_followers_mail_message_subtype_rel rel ON fol.id=rel.mail_followers_id WHERE rel.mail_message_subtype_id=%s AND fol.active=TRUE AND fol.partner_id=%s AND fol.write_date <= %s""" % (attention_id, partner_id, deadline_date)
  ```

15. write 方法重写：

  ```python
  @api.one
  def write(self, val):
      result = super(all_form_design_menu, self).write(val)
      if self.menu_id:
          menu_var = self.env['ir.ui.menu'].browse(self.menu_id.id)
          menu_var.write({'name': self.name})
          return result
  ```

16. 添加 function tool，在 debug 模式下，添加 function tool item，model 为 all.form.design，类型为 method，方法名称为：add_state_change_date_field

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

  ​

17. 旧API接口调用新API接口函数，需要补齐 **cr, uid, context=None** 三个参数

18. self.ensure_one()

  ```python
  """checks that the recordset is a singleton (only contains a single record), raises an error otherwise:"""
  records.ensure_one()
  # is equivalent to but clearer than:
  assert len(records) == 1, "Expected singleton"
  ```

19. 确保入参是 list 类型

  ```python
   if isinstance(ids, (int,long)): 
   	ids = [ids]
  ```

20. Odoo 对象成员赋值 （=）时会调用 write 方法，可以通过中间变量代替：

  ```python
  instance = self.env[attention['res_model']].browse(attention['res_id'])
  # instance.state_change_date = instance.write_date ， 修改为以下代码
  instance_state_change_date = instance.state_change_date
  if not instance_state_change_date:
      instance_state_change_date = instance.write_date
  ```

21. 手动调用 query = 'alter table x_fx__2016_0015 add x_state_change_date date;' 与 self.env['ir.model.fields'].create(vals) 方式添加一列与一个字段，列名称（字段名称）必须以 **x_** 开头。

22. 翻译问题，比如动态model名称，_(‘Description’) 类型，可以通过导出po文件查看，然后进行修改。_() 函数会调用po文件所对应的翻译。

  ```po
   #. module: all_form_design
   #: code:addons/all_form_design/all_form_design.py:1765
   #, python-format
   msgid "Date of state change"
   msgstr "状态变更日期"
  ```

23. xml 继承拓展问题：

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

24. 取today的方法

  ```python
  # 1.   
  from openerp import fields
  from openerp.fields import Date
  today = fields.date.context_today(self, cr, uid, context=context) # 旧API，# (日期时间)
  today = Date.from_string(Date.today())
  # 2.    
  from datetime import date
  today = date.today()
  # 3.    
  import datetime
  today = datetime.datetime.strptime(fields.Date.context_today(self), '%Y-%m-%d')
  today = datetime.datetime.today().strftime("%Y-%m-%d")

  now_time = datetime.datetime.now()  # (only日期)
  now_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
  today = now_time.strftime('%Y-%m-%d')
  # 4.   
  yesterday = (datetime.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
  tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
  ```

25. 定时任务

       ```xml
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

26. **_search()** 方法，所有 search(), name_search(), 最后到会调用 **_search()** 方法，以下是重写**_search()** 的一个示例：（search(), 为通过过滤器，action_widonw 加载时调用的； name_search() 是作为 many2one 字段时调用的）

       ```python
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

27. sql 递归查询

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

35. 递归查询无效子部门

```python
def init_Department(self, department_list):
        """
        先构造部门节点，再构造部门上下级关系
        :param department_list:
        :return:
        """

        # 存储由于父部门未在使用，使的其下所有子部门都不显示
        invalid_dep_ids = []

        for dept in department_list:
            # 判断当前部门的父部门是否在使用
            for d in department_list:
                # 当前部门在使用
                if dept[2] is None or dept[2] == d[0]:
                    break
            # 如果没有在使用，保存当前部门 id，
            else:
                invalid_dep_ids.append(dept[0])
                continue

            dept_node = Department_Node()
            dept_node.add_Department_Node(dept)
            self.department_nodes.append(dept_node)

        # invalid_dep_ids 节点下所有节点，包括子、孙。。。都不显示
        for id in invalid_dep_ids:
            for department_node in self.department_nodes:
                if id == department_node.parent_id:
                    invalid_dep_ids.append(department_node.id)
                    self.department_nodes.remove(department_node)

        for ind, dept_node in enumerate(self.department_nodes):
            self.department_node_index_dict.update({dept_node.id: ind})
            # 保存部门经理的关系后续再建立
            if dept_node.manager_id:
                self.department_manager_id.append((dept_node.manager_id, dept_node))

        for dept_node in self.department_nodes:
            if dept_node.parent_id:
  self.department_nodes[self.department_node_index_dict[dept_node.parent_id]].add_Child_Department(dept_node)
            else:
                self.root_nodes.append(dept_node)
```

36. workflow 中 validate（）

```python
def validate(self, signal):
    result = False
    # ids of all active workflow instances for a corresponding resource (id, model_nam)
    self.cr.execute('select id from wkf_instance where res_id=%s and res_type=%s and state=%s', (self.record.id, self.record.model, 'active'))
    # TODO: Refactor the workflow instance object
    for (instance_id,) in self.cr.fetchall():
        wi = WorkflowInstance(self.session, self.record, {'id': instance_id})

        res2 = wi.validate(signal)

        result = result or res2
        return result
```

抛出 **最大递归深度** 错误（RuntimeError: maximum recursion depth exceeded while calling a Python obj），需要升级 **asteval 库**：`pip install --upgrade asteval`

关于 asteval ：项目中有复杂的业务，后台代码并不能实现所有可能的情况，故此引入了asteval，用于将复杂的业务逻辑写在 python code 中，用 asteval 去执行。

37. 控制视图是否可以创建、修改、删除，以及 item 的颜色


```xml
<record id="employee_dimission_summary_tree" model="ir.ui.view">
  <field name="name">employee.dimission.summary.tree</field>
  <field name="model">dimission.summary</field>
  <field name="arch" type="xml">
    <tree string="Leave" fonts="bold:state=='draft'" colors="green:state=='conform';gray:state in ('reject','cancel');" create="false" edit="true" delete="false">
      <field name="name"/>
      <field name="employee_number"/>
      <field name="employee_name" />
      <field name="department_id"/>
      <field name="create_date"/>
      <field name="leave_time"/>
      <field name="state"/>
      <!--<button string="审批" type="object" class="oe_highlight"></button>-->
    </tree>
  </field>
</record>
```

38.    菜单老权限

       1. 用户管理 -> 组：把相应用户添加的相应的组，以便在访问控制列表中添加组有效

          2. 安全 -> 访问控制列表：添加对应model可访问的组
          3. 用户界面 -> 菜单项: 给对应菜单添加组

39. 对象属性类型

  ```python
  record._columns['approver_ids']._type  # 属性基本类型(field)，为字段类型
  record._columns['approver_ids']._obj   # 属性数据类型(model)，为model名
  ```

40. self

  ```python
   # self
   self.__last_update # 具体record才有
   self._columns # model 所有属性，即列
   self._all_columns # 同上
   self._context # 环境变量 context
   self._cr 
   self._default # 字段默认值
   self._description # model 的 description
   self._fields # 所有字段
   self._ids 
   self._inherit
   self._inherits
   self._name
   self._model
   self._module
   self._rec_name
   self._table # 对应数据表名称
   self._uid
   self.env
   self.id
   self.ids
   self.pool

   # self.env
   self.env.context
   self.env.cr
   self.env.lang
   self.env.uid
  ```

41. Mac 安装 pymssql               


```shell
FreeTDS
brew install freetds  # brew unlink freetds; brew install homebrew/versions/freetds091

Cython
pip install cython

pyssql
pip install pysmsql 
```

42.    在 XML 中，有 5 个预定义的实体引用：

       | `&lt;`   | <    | 小于   |
       | -------- | ---- | ---- |
       | `&gt;`   | >    | 大于   |
       | `&amp;`  | &    | 和号   |
       | `&apos;` | '    | 单引号  |
       | `&quot;` | "    | 引号   |

                        >  注释：在 XML 中，只有字符 "<" 和 "&" 确实是非法的。大于号是合法的，但是用实体引用来代替它是一个好习惯。

43. 代码小结，如 personnel_detail 目录下代码：

            1.    personnel_detail.py 是一个抽象 model，它定义了具体 model 如 hr.termination 等中的公共字段，以及在前后端通信中可能被用的公共方法
            2.    personnel_detail_controller.py 是前后端通信的接口，通过参数类型定义具体 model 与方法，对外隐藏具体信息
                  3.    hr_termination.py 是 personnel.detail 的一个具体实例，按需重新字段或者方法

44. xml 中搜索视图，多条件过滤时 domain 中默认 & 操作需要显示给出，即需要 `&amp;`

  ```xml

   <record model="ir.ui.view" id="rank_job_transfer_search_view">
     <field name="name">rank.job.transfer.search</field>
     <field name="model">rank.job.transfer</field>
     <field name="arch" type="xml">
       <search string="Organizational Adjustment">
         <field name="employee_name"/>
         <field name="employee_number"/>
         <field name="employee_id" string="UserName" filter_domain="[('employee_id.user_id.login','ilike',self)]"/>
         <field name="department_id" string="Org Unit"/>
         <field name="job_id" string="Job"/>
         <field name="transfer_date"/>
         <field name="state"/>
         <filter name="active_employee" string="Active" domain="['&', ('employee_id.work_activity', '=', 'in_service'), ('employee_id.active', '=', True)]"/>
         <filter name="inactive_employee" string="Inactive" domain="['&',('employee_id.work_activity', '=', 'turn_over'), ('employee_id.active', '=', True)]"/>
       </search>
     </field>
   </record>
  ```

45. search 视图

  ```xml

   <record id="rank_job_transfer_team_search_view" model="ir.ui.view">
     <field name="name">rank.job.transfer.team.search.view</field>
     <field name="model">rank.job.transfer</field>
     <field name="priority">32</field>
     <field name="arch" type="xml">
       <search>
         <field name="employee_id" invisible="1"/>
         <filter name="active_employee" string="Active" domain="[('employee_id.work_activity', '=', 'in_service'), ('employee_id.active', '=', True)]"/>
         <filter name="inactive_employee" string="Inactive" domain="[('employee_id.work_activity', '=', 'turn_over'), ('employee_id.active', '=', True)]"/>
         <separator/> <!-- 分割条件 上下部分各自为或关系-->
         <filter string="In Approval" name="state1" domain="[('state','=','waiting'),('approver_ids','=',uid)]" />
         <filter string="Approved" name="state2" domain="[('state','=','done')]" />
         <filter string="Rejected" name="state3" domain="[('state','=','reject')]" />
         <filter string="Cancelled" name="state4" domain="[('state','=','cancel')]" />
         <filter string="Rollback" name="state5" domain="[('state','=','rollback')]" />
       </search>
     </field>
   </record>

   <record model="ir.ui.view" id="rank_job_transfer_search_view">
     <field name="name">rank.job.transfer.search</field>
     <field name="model">rank.job.transfer</field>
     <field name="arch" type="xml">
       <search string="Organizational Adjustment">
         <field name="employee_name"/>
         <field name="employee_number"/>
         <field name="employee_id" string="UserName" filter_domain="[('employee_id.user_id.login','ilike',self)]"/>
         <field name="department_id" string="Org Unit"/>
         <field name="job_id" string="Job"/>
         <field name="transfer_date"/>
         <field name="state"/>
         <filter name="active_employee" string="Active" domain="[('employee_id.work_activity', '=', 'in_service'), ('employee_id.active', '=', True)]"/>
         <filter name="inactive_employee" string="Inactive" domain="[('employee_id.work_activity', '=', 'turn_over'), ('employee_id.active', '=', True)]"/>
       </search>
     </field>
   </record>

   <record model="ir.actions.act_window" id="action_rank_job_transfer_view">
     <field name="name">Organizational Adjustment</field>
     <field name="type">ir.actions.act_window</field>
     <field name="res_model">rank.job.transfer</field>
     <field name="view_type">form</field>
     <field name="view_mode">tree,form,pivot,graph</field>
     <field name="context">{'search_default_active_employee': 1, 'all_employee': 1, 'readonly_bypass': True}</field>
   </record>
   <!-- search_default_active_employee 默认搜索为 search视图中，field name 是 active_employee 的-->
  ```

46. 模块文件整理检查

  ```shell
   find ehr_addons -name *.xml | xargs grep 'model="eroad.menu.access.list"' > ~/Desktop/check_files.log
   awk '/\/data\//{print $1}' ~/Desktop/check_files.log 
  ```

47. many2many 计算失效用户

  ```python
  (lenenterprise_chat_record.with_context(active_test=False).participants)
  ```

48. sql 查询部门员工数

  ```sql
   -- 递归查询，包含子部门人数
   sql = """UPDATE hr_department dep SET now_num=(SELECT count(id) From hr_employee AS emp
   WHERE emp.work_activity='in_service' AND emp.active=TRUE AND emp.department_id in
   (WITH RECURSIVE r AS (
   SELECT * FROM hr_department WHERE id=dep.id
   UNION ALL
   SELECT hr_department.* FROM hr_department, r WHERE hr_department.parent_id = r.id AND hr_department.active=True

   SELECT id FROM r ORDER BY id)
   )
   RETURNING id,now_num
   """
   --只包含当前部门人数
   sql = """UPDATE hr_department dep SET now_num=(SELECT count(id) From hr_employee AS emp
   WHERE emp.work_activity='in_service' AND emp.active=TRUE AND emp.department_id=dep.id)
   RETURNING id,now_num
   """
  ```

49. many2many
          (0,0,{values}) 根据values里面的信息新建一个记录。
          (1,ID,{values})更新id=ID的记录（写入values里面的数据）
          (2,ID) 删除id=ID的数据（调用unlink方法，删除数据以及整个主从数据链接关系）
          (3,ID) 切断主从数据的链接关系但是不删除这个数据
          (4,ID) 为id=ID的数据添加主从链接关系。
          (5) 删除所有的从数据的链接关系就是向所有的从数据调用(3,ID)
          (6,0,[IDs]) 用IDs里面的记录替换原来的记录（就是先执行(5)再执行循环IDs执行（4,ID））
          例子[(6, 0, [8, 5, 6, 4])] 设置 many2many to ids [8, 5, 6, 4]
          one2many
          (0, 0,{ values })根据values里面的信息新建一个记录。
          (1,ID,{values}) 更新id=ID的记录（对id=ID的执行write 写入values里面的数据）
          (2,ID) 删除id=ID的数据（调用unlink方法，删除数据以及整个主从数据链接关系）

50. AES 解密


```python
from Crypto.Cipher import AES
import base64

@classmethod
def decrpyt(cls, pwd):
    obj2 = AES.new('1234567890abcdef', AES.MODE_ECB)
    password = obj2.decrypt(base64.b64decode(pwd))
    for item in ('\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09', '\x0a', '\x0b', '\x0c', '\x0d', '\x0e', '\x0f', '\x10', '\n'):
        password = password.replace(item, '')
        return password

@classmethod
def trans_pwd(cls, pwd):
    """
    App 端传来的 AES 加密的密码解密成明文
    :param pwd:
    :return:
    """
    decrypter = AES.new('1234567890abcdef', AES.MODE_ECB)
    password = decrypter.decrypt(base64.b64decode(pwd)).decode()
    forbidden = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 10)
    password = password.translate(dict(zip(forbidden, [None] * len(forbidden))))
    return password
```

