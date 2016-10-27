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

3. 初始化数据，通常是在 data/ 目录下，通过 xml 或者 json文件的方式。xml 中通过

   ```
   <data noupdate="1">
     <record id="bank_identification_number_type_001" model="bank.identification.number.type">
       <field name="no">1</field>
       <field name="name">ABA Number</field>
     </record>
   </data>
   ```

   方式添加。noupdate="1"。

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

12.   数据库查询 select语句：SELECT  * from table_name where id='id';

13.   修改数据：

     ```sql
     UPDATE ir_translation SET value='员工标签' WHERE lang='zh_CN' and src='Categories' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='category_ids' and model='hr.employee');
     ```

14.   数据库左连接查询：

     ```sql
     """ SELECT fol.id,fol.res_model,fol.res_id FROM mail_followers fol LEFT JOIN mail_followers_mail_message_subtype_rel rel ON fol.id=rel.mail_followers_id WHERE rel.mail_message_subtype_id=%s AND fol.active=TRUE AND fol.partner_id=%s AND fol.write_date <= %s""" % (attention_id, partner_id, deadline_date)
     ```

15.   write 方法重写：

     ```python
     @api.one
     def write(self, val):
         result = super(all_form_design_menu, self).write(val)
         if self.menu_id:
             menu_var = self.env['ir.ui.menu'].browse(self.menu_id.id)
             menu_var.write({'name': self.name})
             return result
     ```

16.   添加 function tool，在 debug 模式下，添加 function tool item，model 为 all.form.design，类型为 method，方法名称为：add_state_change_date_field

     ```python
     @api.model
     def add_state_change_date_field(self):
         # 用来处理旧的e表单数据没有说明字段的问题
         form_design_objs = self.env['all.form.design'].search([])
         for form_design_obj in form_design_objs:
             has_state_change_date = filter(lambda x: x.name in ['state_change_date'], form_design_obj.ir_model_id.field_id)  # TODO 最好用sql?
                 if not has_state_change_date:
                     query = 'alter table %s add state_change_date date;' % form_design_obj.ir_model_id.model
                     self._cr.execute(query)
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

17.   旧API接口调用新API接口函数，需要补齐 **cr, uid, context=None** 三个参数

18.   self.ensure_one()

     ```python
     """checks that the recordset is a singleton (only contains a single record), raises an error otherwise:"""
     records.ensure_one()
     # is equivalent to but clearer than:
     assert len(records) == 1, "Expected singleton"
     ```

19.   确保入参是 list 类型

     ```python
     if isinstance(ids, (int,long)): 
     	ids = [ids]
     ```

     ​