-- 修改翻译：
insert into hr_contract_agreement_category (category, code, name, active) values ('labor_contract', 'CN01', 'Labor Contract', true);
insert into hr_contract_agreement_category (category, code, name, active) values ('agreement', 'CN02', 'None Disclosure Agreement', true);
insert into hr_contract_agreement_category (category, code, name, active) values ('agreement', 'CN03', 'Competitive Restriction', true);
insert into hr_contract_agreement_category (category, code, name, active) values ('agreement', 'CN04', 'Service Agreement', true);

-- 合同协议类型
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('zh_CN', 'Labor Contract', 'hr.contract.agreement.category,name', 1, 'hr_contract_inherit', 'translated', '劳动合同', 'model', true);
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('en_US', 'Labor Contract', 'hr.contract.agreement.category,name', 1, 'hr_contract_inherit', 'translated', 'Labor Contract', 'model', true);

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('zh_CN', 'None Disclosure Agreement', 'hr.contract.agreement.category,name', 2, 'hr_contract_inherit', 'translated', '保密协议', 'model', true);
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('en_US', 'None Disclosure Agreement', 'hr.contract.agreement.category,name', 2, 'hr_contract_inherit', 'translated', 'None Disclosure Agreement', 'model', true);

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('zh_CN', 'Competitive Restriction', 'hr.contract.agreement.category,name', 3, 'hr_contract_inherit', 'translated', '竟业协议', 'model', true);
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('en_US', 'Competitive Restriction', 'hr.contract.agreement.category,name', 3, 'hr_contract_inherit', 'translated', 'Competitive Restriction', 'model', true);

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('zh_CN', 'Service Agreement', 'hr.contract.agreement.category,name', 4, 'hr_contract_inherit', 'translated', '服务期协议', 'model', true);
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) VALUES ('en_US', 'Service Agreementt', 'hr.contract.agreement.category,name', 4, 'hr_contract_inherit', 'translated', 'Service Agreement', 'model', true);

-- 合同&协议模板
UPDATE ir_translation SET is_customer=false WHERE src='Contract Template' AND name in ('ir.ui.menu,name', 'ir.actions.act_window,name') AND module='eroad_template';
UPDATE ir_translation SET is_customer=false WHERE src='Contract Template Name' or value='Contract Template Name' AND name='ir.model.fields,field_description' AND module='eroad_template';
UPDATE ir_translation SET is_customer=false WHERE src='Template Remind' or value='Template Remind' AND name='ir.model.fields,field_description' AND module='eroad_template';

-- 合同
UPDATE ir_translation SET is_customer=false WHERE src='Contract ID' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=false WHERE src='Category' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=false WHERE src='Validity' AND name='ir.ui.view,arch_db' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=false WHERE src='Category Name' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=false WHERE src='template' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';

DELETE FROM ir_translation WHERE src IN ('Draft data', 'Created data') AND module='hr_contract_inherit' AND name='ir.ui.view,arch_db';

-- 合同&协议模板
UPDATE ir_translation SET is_customer=true WHERE src='Contract Template' AND name in ('ir.ui.menu,name', 'ir.actions.act_window,name') AND module='eroad_template';
UPDATE ir_translation SET is_customer=true WHERE src='Contract Template Name' or value='Contract Template Name' AND name='ir.model.fields,field_description' AND module='eroad_template';
UPDATE ir_translation SET is_customer=true WHERE src='Template Remind' or value='Template Remind' AND name='ir.model.fields,field_description' AND module='eroad_template';

-- 合同
UPDATE ir_translation SET is_customer=true WHERE src='Contract ID' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=true WHERE src='Category' AND name='ir.model.fields,field_description' AND module='hr_contract_inherit';
UPDATE ir_translation SET is_customer=true WHERE src='Validity' AND name='ir.ui.view,arch_db' AND module='hr_contract_inherit';

UPDATE ir_translation SET value='模板主题' WHERE lang='zh_CN' AND src='Template Subject' AND name='ir.model.fields,field_description' AND module='eroad_template';

UPDATE ir_translation SET value='合同与协议模板' WHERE lang='zh_CN' AND src in ('Contract & Agreement Template', 'Contract &amp; Agreement Template') AND name in ('ir.ui.menu,name', 'ir.actions.act_window,name') AND module='eroad_template';

UPDATE ir_translation SET value='类型' WHERE src='Category' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='eroad_template';

-- 删除约束
ALTER TABLE eroad_template_preview DROP CONSTRAINT eroad_template_preview_name_category_uniq;
ALTER TABLE eroad_template DROP CONSTRAINT eroad_template_name_category_uniq;

UPDATE ir_translation SET value='劳动合同', is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Labor Contract' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET value='保密协议', is_customer=true, state='translated' WHERE lang='zh_CN' AND src='None Disclosure Agreement' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET value='竟业协议', is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Competitive Restriction' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET value='服务期协议', is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Service Agreement' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';


UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='en_US' AND src='Labor Contract' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='en_US' AND src='None Disclosure Agreement' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='en_US' AND src='Competitive Restriction' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='en_US' AND src='Service Agreement' AND name='hr.contract.agreement.category,name' AND module='hr_contract_inherit' AND type='model';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Labor Contract' AND name='hr.contract.agreement.category,category' AND module='hr_contract_inherit' AND type='selection';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='zh_CN' AND src='None Disclosure Agreement' AND name='hr.contract.agreement.category,category' AND module='hr_contract_inherit' AND type='selection';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Competitive Restriction' AND name='hr.contract.agreement.category,category' AND module='hr_contract_inherit' AND type='selection';

UPDATE ir_translation SET is_customer=true, state='translated' WHERE lang='zh_CN' AND src='Service Agreement' AND name='hr.contract.agreement.category,category' AND module='hr_contract_inherit' AND type='selection';

SELECT * from ir_translation WHERE src='New Job Grade Category' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
SELECT * from ir_translation WHERE src='New Job Grade Category' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
SELECT * from ir_translation WHERE src='New Job Grade' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
SELECT * from ir_translation WHERE src='New Job Grade' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';

SELECT * from ir_translation WHERE src='New Job Grade Category' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
SELECT * from ir_translation WHERE src='New Job Grade Category' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
SELECT * from ir_translation WHERE src='New Job Grade' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
SELECT * from ir_translation WHERE src='New Job Grade' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';

UPDATE ir_translation SET value='New Grade' WHERE src='New Job Grade Category' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
UPDATE ir_translation SET value='新职级' WHERE src='New Job Grade Category' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
UPDATE ir_translation SET value='New Level' WHERE src='New Job Grade' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';
UPDATE ir_translation SET value='新级别' WHERE src='New Job Grade' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_rank_job_transfer';

UPDATE ir_translation SET value='New Grade' WHERE src='New Job Grade Category' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
UPDATE ir_translation SET value='新职级' WHERE src='New Job Grade Category' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
UPDATE ir_translation SET value='New Level' WHERE src='New Job Grade' AND lang='en_US' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';
UPDATE ir_translation SET value='新级别' WHERE src='New Job Grade' AND lang='zh_CN' AND name='ir.model.fields,field_description' AND module='hr_employee_rank';

UPDATE ir_translation SET value='草稿' WHERE src='Draft' AND lang='zh_CN' AND name='hr.termination,state' AND module='employee_dimission';

-- 岗位成了职级
DELETE FROM ir_translation WHERE src='Transfer' AND name='ir.model,name' AND module='hr_employee_rank' AND res_id=(SELECT id FROM ir_model WHERE model='employee.rank.adjust');
-- 维塔士 HR Termination
UPDATE ir_translation SET value='员工离职' WHERE src='HR Termination' AND lang='zh_CN' AND name='ir.model,name';


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


-- 删除画面多余 filed
DELETE FROM ir_ui_view WHERE model_data_id in (SELECT id FROM ir_model_data WHERE module='hr_cost_center' AND model='ir.ui.view' AND name in ('view_hr_employee_cost_center_form', 'view_hr_department_cost_center_form', 'view_job_transfer_cost_center_form', 'view_rank_job_transfer_cost_center_form'));

DELETE FROM ir_model_data WHERE module='hr_cost_center' AND model='ir.ui.view' AND name in ('view_hr_employee_cost_center_form', 'view_hr_department_cost_center_form', 'view_job_transfer_cost_center_form', 'view_rank_job_transfer_cost_center_form');

-- 修改初始化数据所属 module
UPDATE ir_model_data SET module='hr_base' WHERE module='hr_cost_center' AND model in ('ir.cron', 'cost.center.type', 'ir.ui.menu');

SELECT * FROM ir_translation T INNER JOIN ir_model S ON T.res_id=S.id WHERE S.model='hr.contract' AND T.src='Contract' AND T.lang='zh_CN';
UPDATE ir_translation SET module='hr_contract_inherit' WHERE res_id=(SELECT id FROM ir_model WHERE model='hr.contract');
UPDATE ir_translation SET module='hr_job_transfer' WHERE src='New Cost Center' AND res_id=(SELECT id FROM ir_model_fields WHERE model='job.transfer' AND name='new_cost_center');
UPDATE ir_translation SET module='hr_rank_job_transfer' WHERE src='New Cost Center' AND res_id=(SELECT id FROM ir_model_fields WHERE model='rank.job.transfer' AND name='new_cost_center');


-- 查询结果作为值插入：
INSERT INTO import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) 
SELECT true, 'many2one', false, 23 , true, i1.id, i2.id, i3.id 
	FROM ir_model_fields i1, ir_model_fields i2, import_excel i3 
WHERE i1.model='hr.employee' AND i1.name='employee_type_rep' AND i2.model='hr.employee.type' AND i2.name='name' AND i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true , 'many2one', false, 23 , true , i1.id , i2.id , i3.id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true as unique_index, 'many2one' as field_type, false as create_if_not_find, 23 as sequence , true as required, i1.id as field_id, i2.id as relation_field, i3.id as import_model_id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';

SELECT * FROM ir_model_fields 
WHERE model IN ('hr.contract', 'employee.dimission', 'hr.termination', 'employee.rank.adjust', 'job.transfer', 'employee.probation') 
AND name='dep_manager';
-- 修改字段关联关系
UPDATE ir_model_fields SET related='department_id.manager_id' 
WHERE model IN ('hr.contract', 'employee.dimission', 'hr.termination', 'employee.rank.adjust', 'job.transfer', 'employee.probation') 
AND name='dep_manager';


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
	create_user_id·		·, create_date, write_uid, write_date, active)
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

--1.插入到hr_termination
INSERT INTO hr_termination(
    name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id,
    dep_manager, leave_time, reason_leave_type, reason_leave, leave_reason,
    social_security_end_month, housing_fund_end_month, 
    state, flow_id, activity_id, submit_date, manager_level, batch, 
    create_uid, create_date, write_uid, write_date, active)
SELECT 
    name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, 
    dep_manager, leave_time, reason_leave_type, reason_leave, leave_reason,
    social_security_end_month, housing_fund_end_month, 
    state, flow_id, activity_id, submit_date, manager_level, batch, 
    create_uid, create_date, write_uid, write_date, active
FROM employee_dimission
WHERE employee_dimission.name IN ('eh201612131038', 'eh201612131040', 'eh201612131039');

--2.插入到dimission_summary
INSERT INTO dimission_summary (
    can_show, is_hr_termination, termination_id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
    leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
    state, flow_id, activity_id, submit_date, manager_level, batch, 
    create_user_id, create_date, write_uid, write_date, active)
SELECT 
    false, true, id, name, employee_id, employee_number, employee_name, company_id, department_id, job_id, parent_id, dep_manager,
    leave_time, reason_leave_type, reason_leave, social_security_end_month, housing_fund_end_month, leave_reason,
    state, flow_id, activity_id, submit_date, manager_level, batch, 
    create_uid, create_date, write_uid, write_date, active
FROM hr_termination WHERE name IN ('eh201612131038', 'eh201612131040', 'eh201612131039');

--3.建立 hr_termination 与 dimission_summar 关联
UPDATE hr_termination SET dimission_summary_id=S.id
FROM (SELECT id, termination_id, name FROM dimission_summary WHERE is_hr_termination=True) S
WHERE hr_termination.id=S.termination_id AND S.name in ('eh201612131038', 'eh201612131040', 'eh201612131039');


UPDATE company_record SET res_model='hr.termination' res_id=S.id
FROM (SELECT id FROM hr_termination WHERE name='eh201612131038') S
WHERE company_record.event_type='leave' 
AND employee_id=(SELECT employee_id from employee_dimission WHERE name='eh201612131038');

UPDATE company_record SET res_model='hr.termination' res_id=S.id
FROM (SELECT id FROM hr_termination WHERE is_hr_termination=True) S
WHERE company_record.event_type='leave' 
AND employee_id IN (SELECT employee_id from employee_dimission WHERE name IN ('eh201612131038', 'eh201612131039', 'eh201612131040'));


-- 更新 action_code
update import_excel set action_code='# Available variables' where model_id=(select id from ir_model where model='employee.dimission');


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


-- replace函数：
UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''tz'')', 'env.context.get(''tz'', '''') if env.context.get(''tz'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'env.context.get(''lang'')', 'env.context.get(''lang'', '''') if env.context.get(''lang'', '''') else None') WHERE name='基本信息';

UPDATE import_excel SET action_code = replace(action_code,'''mobile'': login', '''mobile'': employee_value_dict.get(''work_phone'', '''')') WHERE name='基本信息';

UPDATE import_excel SET excel_type = null WHERE name IN ('基本信息', '用户管理', '时间档案', '社保个税');

SELECT design_model FROM all_form_design WHERE active=true;

ALTER TABLE x_af_2016_0002 ADD state_change_date DATE;

UPDATE x_af_2016_0002 SET state_change_date=write_date where state='done';

-- 添加字段
SELECT 'ALTER TABLE ' ||design_model|| ' ADD state_change_date2 DATE;' FROM all_form_design WHERE active=true; 

SELECT 'UPDATE ' ||design_model|| ' SET state_change_date=write_date;' FROM all_form_design WHERE active=true;

SELECT 'ALTER TABLE ' ||design_model|| ' ADD last_approve_date DATE;' FROM all_form_design WHERE active=true; 

SELECT 'ALTER TABLE ' ||design_model|| ' ADD last_approver integer;' FROM all_form_design WHERE active=true; 



--员工离职
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Employee Name</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>员工姓名</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Employee Number</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>员工编号</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Org Unit</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>组织单元</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Job</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>岗位</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Date</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Date</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Date</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>离职日期</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Reason Category</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Reason Category</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Reason Category</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>原因类别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Reason</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Reason</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Reason</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>离职原因</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Remarks:<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '备注：<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Employee Name', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '员工姓名', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Org Unit', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '组织单元', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Job', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Job', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Job', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '岗位', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Approval Node', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '审批节点', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Status', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Status', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Status', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '状态', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Time', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Time', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Time', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '时间', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Remarks', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '备注', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Termination', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Termination', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Termination', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '员工离职', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Signature:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '签字：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Date:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '日期：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Email:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Email:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Email:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '电子邮件：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Fax:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '传真：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Page:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Page:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Page:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '页：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Phone:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '电话:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Website:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Website:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Website:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '网站:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_hr_termination';



--离职记录
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Employee Name</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>员工姓名</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Employee Number</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>员工编号</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Org Unit</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>组织单元</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Job</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>岗位</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Date</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Date</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Date</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>离职日期</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Reason Category</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Reason Category</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Reason Category</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>原因类别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Termination Reason</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>Termination Reason</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Termination Reason</span>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '<span>离职原因</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Remarks:<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '备注：<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Employee Name', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '员工姓名', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Org Unit', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '组织单元', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Job', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Job', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Job', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '岗位', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Approval Node', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '审批节点', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Status', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Status', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Status', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '状态', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Time', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Time', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Time', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '时间', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Remarks', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '备注', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Termination', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Termination', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Termination', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '员工离职', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Signature:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '签字：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Date:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '日期：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Email:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Email:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Email:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '电子邮件：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Fax:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '传真：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Page:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Page:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Page:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '页：', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Phone:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '电话:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Website:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', 'Website:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Website:', 'ir.ui.view,arch_db', i1.id, 'employee_dimission', 'translated', '网站:', 'model', true 
FROM ir_ui_view i1 WHERE key='employee_dimission.report_dimission_summary';



--岗位职级调整
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Employee Name</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Name</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>员工姓名</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Employee Number</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Employee Number</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>员工编号</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Org Unit</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>组织单元</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Job</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>岗位</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Effective Date</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Effective Date</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Effective Date</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>生效日期</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Supervisor</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Supervisor</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Supervisor</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>汇报上级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Org Unit Manager</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Org Unit Manager</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Org Unit Manager</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>组织单元经理</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Function</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Function</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Function</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>职能</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Transfer Reason</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Transfer Reason</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Transfer Reason</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>调动类型</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Org Unit</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Org Unit</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新组织单元</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Position</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Position</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Position</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新岗位</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Supervisor</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Supervisor</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Supervisor</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新汇报上级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Org Unit Manager</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Org Unit Manager</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Org Unit Manager</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新组织单元经理</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Function</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Function</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Function</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新职能</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Promotion Reason</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Promotion Reason</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Promotion Reason</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>调整原因</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Remarks:<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks:<br/>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '备注：<br/>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Employee Name', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Employee Name', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '员工姓名', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Org Unit', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Org Unit', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '组织单元', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Job', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Job', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Job', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '岗位', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Approval Node', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Approval Node', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '审批节点', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Status', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Status', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Status', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '状态', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Time', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Time', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Time', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '时间', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Remarks', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Remarks', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '备注', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Signature:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Signature:_____________', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '签字：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Date:_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Date:_____________', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '日期：_____________', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Email:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Email:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Email:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '电子邮件：', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Fax:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Fax:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '传真：', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Page:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Page:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Page:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '页：', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Phone:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Phone:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '电话:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', 'Website:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', 'Website:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', 'Website:', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '网站:', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


-- 除维塔士外
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Job Grade Category</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>职级类别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Job Grade</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>职级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Job Grade Category</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新职级类别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Job Grade</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新职级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


-- 维塔士
INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Grade</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>职级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>Level</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>级别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


SELECT 'en_US', '<span>New Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Grade</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Job Grade Category</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新职级</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';


INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'en_US', '<span>New Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>New Level</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';

INSERT INTO ir_translation (lang, src, name, res_id, module, state, value, type, is_customer) 
SELECT 'zh_CN', '<span>New Job Grade</span>', 'ir.ui.view,arch_db', i1.id, 'hr_rank_job_transfer', 'translated', '<span>新级别</span>', 'model', true 
FROM ir_ui_view i1 WHERE key='hr_rank_job_transfer.report_rank_job_transfer';









