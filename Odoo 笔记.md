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
<field name="model_id" domain="[('transient','=', False)]" options="{'no_create': True, 'no_open': True}"/>                               
<notebook attrs="{'invisible': [('model_id','=', False)]}">