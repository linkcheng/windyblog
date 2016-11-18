修改翻译：
UPDATE ir_translation SET value='Bank Name 1' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='bank_name' and model='hr.employee');

UPDATE ir_translation SET value='Bank Account 1' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='bank_account' and model='hr.employee');

UPDATE ir_translation SET value='Bank Account Holder 1' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='bank_account_holder' and model='hr.employee');

UPDATE ir_translation SET value='Created on' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='create_date' and model='hr.job');

UPDATE ir_translation SET value='Created by' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='create_uid' and model='hr.job');

select value from ir_translation WHERE module='workbench_rebuilt' and res_id=(SELECT id FROM ir_model_fields WHERE name='state_change_date' and model='work.bench');

UPDATE ir_translation SET value='状态变更日期' WHERE lang='zh_CN' and module='workbench_rebuilt' and res_id=(SELECT id FROM ir_model_fields WHERE name='state_change_date' and model='work.bench');

UPDATE ir_translation SET value='状态变更日期' WHERE lang='zh_CN' and module='hr_travel' and res_id=(SELECT id FROM ir_model_fields WHERE name='state_change_date' and model='hr.travel');

UPDATE ir_translation SET value='员工标签' WHERE lang='zh_CN' and src='Categories' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='category_ids' and model='hr.employee');


UPDATE ir_translation SET src='Valid from', value='Valid from' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='start_date' and model='hr.department');

UPDATE ir_translation SET src='Valid to',value='Valid to' WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='end_date' and model='hr.department');

select src,value from ir_translation where lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='end_date' and model='hr.department');

查询：
select value from ir_translation WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='bank_name' and model='hr.employee');


查询结果作为值插入：
INSERT INTO import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) SELECT true, 'many2one', false, 23 , true, i1.id, i2.id, i3.id FROM ir_model_fields i1, ir_model_fields i2, import_excel i3 WHERE i1.model='hr.employee' AND i1.name='employee_type_rep' AND i2.model='hr.employee.type' AND i2.name='name' AND i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true , 'many2one', false, 23 , true , i1.id , i2.id , i3.id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true as unique_index, 'many2one' as field_type, false as create_if_not_find, 23 as sequence , true as required, i1.id as field_id, i2.id as relation_field, i3.id as import_model_id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';


replace函数：
UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''tz'')', 'env.context.get(''tz'', '''') if env.context.get(''tz'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''lang'')', 'env.context.get(''lang'', '''') if env.context.get(''lang'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'''mobile'': login', '''mobile'': employee_value_dict.get(''work_phone'', '''')') WHERE name='基本信息';

UPDATE import_excel SET excel_type = null WHERE name IN ('基本信息', '用户管理', '时间档案', '社保个税');

SELECT design_model FROM all_form_design WHERE active=true;

ALTER TABLE x_af_2016_0002 ADD state_change_date DATE;

UPDATE x_af_2016_0002 SET state_change_date=write_date where state='done';

SELECT 'ALTER TABLE ' ||design_model|| ' ADD state_change_date2 DATE;' FROM all_form_design WHERE active=true; 

SELECT 'UPDATE ' ||design_model|| ' SET state_change_date=write_date;' FROM all_form_design WHERE active=true;


