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
INSERT INTO import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) 
SELECT true, 'many2one', false, 23 , true, i1.id, i2.id, i3.id 
	FROM ir_model_fields i1, ir_model_fields i2, import_excel i3 
WHERE i1.model='hr.employee' AND i1.name='employee_type_rep' AND i2.model='hr.employee.type' AND i2.name='name' AND i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true , 'many2one', false, 23 , true , i1.id , i2.id , i3.id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true as unique_index, 'many2one' as field_type, false as create_if_not_find, 23 as sequence , true as required, i1.id as field_id, i2.id as relation_field, i3.id as import_model_id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';


-- employee_dimission
INSERT INTO dimission_summary (
	can_show, is_hr_termination, dimission_id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
	leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
	state, flow_id, activity_id, submit_date, manager_level, batch, 
	create_uid, create_date, write_uid, write_date, active)
SELECT 
	false, false, id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
	leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
	state, flow_id, activity_id, submit_date, manager_level, batch, 
	create_uid, create_date, write_uid, write_date, active
FROM employee_dimission;

UPDATE employee_dimission SET dimission_summary_id=S.id
FROM (SELECT id, dimission_id FROM dimission_summary WHERE is_hr_termination=False) S
WHERE employee_dimission.id=S.dimission_id;

INSERT INTO approve_notify (
	create_uid, create_date, write_uid, write_date, active, activity_id, description, state, approve_date, 
	user_id, name, department_id, job_id, record_id, model)
SELECT 
	i1.create_uid, i1.create_date, i1.write_uid, i1.write_date, i1.active, i1.activity_id, i1.description, i1.state, i1.approve_date, 
	i1.user_id, i1.name, i1.department_id, i1.job_id, i2.id, 'dimission.summary'
	FROM approve_notify i1, dimission_summary i2
WHERE i1.model='employee.dimission' AND i1.active=TRUE AND i1.record_id=i2.dimission_id;

-- hr_dimission

INSERT INTO hr_termination(
	name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id,
	leave_time, reason_leave_type, reason_leave, leave_reason,
	state, flow_id, activity_id, submit_date, manager_level, batch, 
	create_uid, create_date, write_uid, write_date, active)
SELECT 
	i1.name, i1.employee_id, i2.employee_number, i2.name, i1.company_id, i1.department_id, i1.job_id, i2.parent_id, 
	i1.leave_time, i1.reason_leave_type, i1.reason_leave, i1.dimission_reason,
	i1.state, i1.flow_id, i1.activity_id, i1.submit_date, i1.manager_level, i1.batch, 
	i1.create_uid, i1.create_date, i1.write_uid, i1.write_date, i1.active
	FROM hr_dimission i1, hr_employee i2 
	WHERE i1.employee_id=i2.id;

INSERT INTO dimission_summary (
	can_show, is_hr_termination, termination_id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
	leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
	state, flow_id, activity_id, submit_date, manager_level, batch, 
	create_uid, create_date, write_uid, write_date, active)
SELECT 
	false, true, id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
	leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
	state, flow_id, activity_id, submit_date, manager_level, batch, 
	create_uid, create_date, write_uid, write_date, active
FROM hr_termination;

UPDATE hr_termination SET dimission_summary_id=S.id
FROM (SELECT id, termination_id FROM dimission_summary WHERE is_hr_termination=True) S
WHERE hr_termination.id=S.termination_id;

INSERT INTO approve_notify (
	create_uid, create_date, write_uid, write_date, active, activity_id, description, state, approve_date, 
	user_id, name, department_id, job_id, record_id, model)
SELECT 
	i1.create_uid, i1.create_date, i1.write_uid, i1.write_date, i1.active, i1.activity_id, i1.description, i1.state, i1.approve_date, 
	i1.user_id, i1.name, i1.department_id, i1.job_id, i2.id, 'dimission.summary'
	FROM approve_notify i1, dimission_summary i2
WHERE i1.model IN ('hr.termination', 'hr.dimission') AND i1.active=TRUE AND i1.record_id=i2.termination_id;


-- 翻译
UPDATE ir_translation SET value='组织单元' WHERE lang='zh_CN' AND src='Org Unit' AND module='employee_dimission' AND value='部门';

UPDATE ir_translation SET value=replace(value, ' has rejected the termination request', '拒绝了您提交的的员工离职申请') WHERE position('has rejected the termination request' in src)>0 AND lang='zh_CN'; 

UPDATE ir_translation SET value=replace(value, ' has submitted a termination request', '提交了员工离职申请') WHERE position('has submitted a termination request' in src)>0 AND lang='zh_CN'; 

UPDATE ir_translation SET value=replace(value, 'The termination request has been approved', '您提交的一条员工离职申请已审批通过') WHERE position('The termination request has been approved' in src)>0 AND lang='zh_CN'; 


UPDATE Table_A  T
SET T.LatestTM=S.TM， T.LatestData=S.Data
FROM 
(select A.ID, B.TM, A.DATA
from TABLE_B A,
JOIN (select B.ID,MAX(B.TM) from TABLE_B B group by B.ID) C
ON A.ID = C.ID
) S
where Table_A.ID = S.ID


replace函数：
UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''tz'')', 'env.context.get(''tz'', '''') if env.context.get(''tz'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''lang'')', 'env.context.get(''lang'', '''') if env.context.get(''lang'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'''mobile'': login', '''mobile'': employee_value_dict.get(''work_phone'', '''')') WHERE name='基本信息';

UPDATE import_excel SET excel_type = null WHERE name IN ('基本信息', '用户管理', '时间档案', '社保个税');

SELECT design_model FROM all_form_design WHERE active=true;

ALTER TABLE x_af_2016_0002 ADD state_change_date DATE;

UPDATE x_af_2016_0002 SET state_change_date=write_date where state='done';

添加字段
SELECT 'ALTER TABLE ' ||design_model|| ' ADD state_change_date2 DATE;' FROM all_form_design WHERE active=true; 

SELECT 'UPDATE ' ||design_model|| ' SET state_change_date=write_date;' FROM all_form_design WHERE active=true;

SELECT 'ALTER TABLE ' ||design_model|| ' ADD last_approve_date DATE;' FROM all_form_design WHERE active=true; 

SELECT 'ALTER TABLE ' ||design_model|| ' ADD last_approver integer;' FROM all_form_design WHERE active=true; 
