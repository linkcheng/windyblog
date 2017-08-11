update ir_model_data set module='resource' where name='field_resource_calendar_name';


DO $$
BEGIN
IF EXISTS(SELECT * FROM information_schema.columns WHERE table_name='hr_remind_python_code') THEN
	DELETE FROM ir_model_data WHERE model='ir.model.access' and res_id in (SELECT id FROM ir_model_access WHERE name='hr_remind_python_code');
	DELETE FROM ir_model_access WHERE name='hr_remind_python_code';
	DELETE FROM ir_model_data WHERE model='hr.remind.python.code';
	DELETE FROM ir_model_fields WHERE model='hr.remind.python.code';
	DELETE FROM ir_model_constraint WHERE name like 'hr_remind_python_code%';
	DELETE FROM ir_model WHERE model='hr.remind.python.code';
	ALTER TABLE hr_remind_config DROP COLUMN python_code;
	DROP TABLE hr_remind_python_code;
END IF;
END $$;

-- 删除总表审批通知
delete from approve_notify where model='dimission.summary' and record_id in (
	select id from dimission_summary 
		where id in (select dimission_summary_id from employee_dimission where state in ('reject', 'cancel'))
		or id in (select dimission_summary_id from hr_termination where state in ('reject', 'cancel'))
);

-- 删除总表记录
delete from dimission_summary 
	where id in (select dimission_summary_id from employee_dimission where state in ('reject', 'cancel'))
	or id in (select dimission_summary_id from hr_termination where state in ('reject', 'cancel'));

-- 删除离职通知
delete from approve_notify where model='hr.termination' and record_id in (
	select id from hr_termination where state in ('reject', 'cancel')
);

delete from approve_notify where model='employee.dimission' and record_id in (
	select id from employee_dimission where state in ('reject', 'cancel')
);

-- 删除离职记录
delete from hr_termination where state in ('reject', 'cancel');
delete from employee_dimission where state in ('reject', 'cancel');

update mail_message set active=false where model='hr.expense.expense' and res_id in 
(select id from hr_expense_expense where employee_id in (select id from hr_employee where employee_number like 'C%' or employee_number like 'X%') and sequence not in ('EA201706082634', 'EA201706072630'));

update mail_followers set active=false where res_model='hr.expense.expense' and res_id in 
(select id from hr_expense_expense where employee_id in (select id from hr_employee where employee_number like 'C%' or employee_number like 'X%') and sequence not in ('EA201706082634', 'EA201706072630'));

update ir_model_data set name='placeholder_27', module='hr_base' where name='placeholder_01' and module='hr_employee_search_extension';

DO $$
BEGIN
IF NOT EXISTS(SELECT * FROM app_action WHERE module = 'employee_certification' AND action='eHR://certification_create' AND model='employee.certification') THEN
    INSERT INTO app_action (sequence, module_installed, module, icon_url, app_module, app_title, description, show_type, name, action, model)
    VALUES (120, 't', 'employee_certification', '/eroad_app_action/static/src/img/show_create/certification_create.png', 'certification_create', 'Certification', '创建员工证明', 'show_create', '员工证明', 'eHR://certification_create', 'employee.certification');
    INSERT INTO ir_translation (lang, src, name, res_id, state, value, type)
    SELECT 'zh_CN', 'Certification', 'app.action,app_title', s.id, 'translated', '员工证明', 'model' FROM app_action s WHERE app_title='Certification';
END IF;
END $$;

insert into app_action (sequence, module_installed, module, icon_url, app_module, app_title, description, show_type, name, action, model) 
values (120, 't', 'employee_certification', '/eroad_app_action/static/src/img/show_create/certification_create.png', 'certification_create', 'Certification', '创建员工证明', 'show_create', '员工证明', 'eHR://certification_create', 'employee.certification');
insert into ir_translation (lang, src, name, res_id, state, value, type) 
select 'zh_CN', 'Certification', 'app.action,app_title', s.id, 'translated', '员工证明', 'model' from app_action s where app_title='Certification';

update hr_employee emp set department_id=s.department_id, job_id=s.job_id from (
select cr.employee_id, cr.department_id, cr.job_id from company_record cr where cr.res_model='job.transfer' and cr.validate_date='2017-05-01' 
and cr.res_id in (select id from job_transfer jt where jt.start_date='2017-05-01' and jt.name between 'JT201705152924' and 'JT201705152949')) s
where emp.id=s.employee_id;

update ir_cron set model='hr.remind.config.manager' where function='execute_remind_task';

update app_message_template set model_id = (select id from ir_model where model='hr.remind.config') where code='T001';

insert into ir_translation (lang, src, name, res_id, state, value, type)
values ('zh_CN', 'APP Employee Birthday Wishes', 'app.message.template,name', 1, 'translated', 'APP员工生日祝福', 'model');

insert into ir_translation (lang, src, name, res_id, state, value, type)
values ('zh_CN', 'APP Employee Birthday Wishes', 'app.message.template,subject', 1, 'translated', 'APP员工生日祝福', 'model');

insert into ir_translation (lang, src, name, res_id, state, value, type)
values ('zh_CN', 'Dear ${obj.employee_id.name},
Happy birthday! We wish you all the happiness, wealth and health!
Yours Sincerely', 'app.message.template,content', 1, 'translated', '亲爱的${obj.employee_id.name}， 
在这个特别的日子里，公司为你送上最诚挚的祝福！祝你生日快乐，健康幸福～～ 
你诚挚的', 'model');

delete from ir_translation where src='Personal birthday wishes';

--virtuas
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
values ('en_US', 'New Job Grade', 'addons/hr_rank_job_transfer/rank_job_transfer.py', 458, 'hr_rank_job_transfer', 'translated', 'New Level', 'code');
update ir_translation set value='新级别' where src='New Job Grade' and module='hr_rank_job_transfer' and lang='zh_CN' and name='addons/hr_rank_job_transfer/rank_job_transfer.py';

insert into ir_translation (lang, src, name, res_id, module, state, value, type)
values ('en_US', 'New Job Grade', 'addons/hr_employee_rank/employee_rank_adjust.py', 416, 'hr_employee_rank', 'translated', 'New Level', 'code');
update ir_translation set value='新级别' where src='New Job Grade' and module='hr_employee_rank' and lang='zh_CN' and name='addons/hr_employee_rank/employee_rank_adjust.py';

insert into ir_translation (lang, src, name, res_id, module, state, value, type)
values ('en_US', 'New Job Grade Category', 'addons/hr_employee_rank/employee_rank_adjust.py', 409, 'hr_employee_rank', 'translated', 'New Grade', 'code');
update ir_translation set value='新职级' where src='New Job Grade Category' and module='hr_employee_rank' and lang='zh_CN' and name='addons/hr_employee_rank/employee_rank_adjust.py';

delete from ir_translation where src='Current user has no employee record, please change employee to apply!';
delete from ir_translation where src='list show must not be binary or lines';

-- 删除序列号规则
delete from ir_sequence where name='Employee Birthday Wishes';

-- 删除原来员工祝福的表
delete from ir_model_fields where model in ('employee.birthday.wish', 'employee.birthday.wish.config');
delete from ir_model_data where model='ir.model' and name in ('employee.birthday.wish', 'employee.birthday.wish.config');
delete from ir_model_constraint where name like 'employee_birthday_wish%';
delete from ir_model where model in ('employee.birthday.wish', 'employee.birthday.wish.config');
drop table employee_birthday_wish;
drop table employee_birthday_wish_config;

-- 邮件模板历史数据修改
update mail_template set subject='Work anniversary wishes' where name='员工工作周年祝福';
delete from ir_translation where src='Work anniversary wishes' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Work anniversary wishes', 'mail.template,subject', a.id, 'hr_remind', 'translated', '工作周年祝福', 'model'
from mail_template a where name='员工工作周年祝福';

update mail_template set subject='Birthday wishes' where name='个人生日祝福';
delete from ir_translation where src='Personal birthday wishes' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Birthday wishes', 'mail.template,subject', a.id, 'hr_remind', 'translated', '生日祝福', 'model'
from mail_template a where name='个人生日祝福';

delete from ir_translation where src like '
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")}%
% else:
    %' and name='mail.template,subject' and module='hr_remind';


update mail_template set subject='Employee Service Anniversary Reminder' where name='员工服务公司周年提醒';
delete from ir_translation where src='
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")}月员工工作周年提醒
% else:
    员工工作周年提醒
% endif
            ' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Employee Service Anniversary Reminder', 'mail.template,subject', a.id, 'hr_remind', 'translated', '员工工作周年提醒', 'model'
from mail_template a where name='员工服务公司周年提醒';


update mail_template set subject='Expiry Reminder' where name='证件到期提醒';
delete from ir_translation where src='
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")} 证件到期提醒(Month)
% else:
    证件到期提醒
% endif
            ' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Expiry Reminder', 'mail.template,subject', a.id, 'hr_remind', 'translated', '员工证件到期提醒', 'model'
from mail_template a where name='证件到期提醒';


update mail_template set subject='Probation Reminder' where name='试用期转正提醒';
delete from ir_translation where src='
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")}月员工转正提醒
% else:
    员工转正提醒
% endif
            ' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Probation Reminder', 'mail.template,subject', a.id, 'hr_remind', 'translated', '员工转正提醒', 'model'
from mail_template a where name='试用期转正提醒';


update mail_template set subject='Contract Expiry Reminder' where name='合同提醒';
delete from ir_translation where src='
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")}月员工合同到期提醒
% else:
    员工合同到期提醒
% endif
            ' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Contract Expiry Reminder', 'mail.template,subject', a.id, 'hr_remind', 'translated', '员工合同到期提醒', 'model'
from mail_template a where name='合同提醒';


update mail_template set subject='Employee Birthday Reminder' where name='生日提醒';
delete from ir_translation where src='
% if ctx.get("time_unit") in ["months"]:
    ${ctx.get("month")}月员工生日提醒
% else:
    员工生日提醒
% endif
            ' and name='mail.template,subject' and module='hr_remind';
insert into ir_translation (lang, src, name, res_id, module, state, value, type)
select 'zh_CN', 'Employee Birthday Reminder', 'mail.template,subject', a.id, 'hr_remind', 'translated', '员工生日提醒', 'model'
from mail_template a where name='生日提醒';



-- pdf 打印历史数据
UPDATE ir_ui_view SET arch_db=replace(arch_db, '<div class="row">
                    <div class="col-xs-12" style="height: 20px;"/>
                </div>', '<div class="row">
                    <div class="col-xs-7">
                    </div>
                    <div class="col-xs-2 text-right" style="height: 20px;">Signature:</div>
                    <div class="col-xs-3 text-left" style="height: 20px;">_____________</div>
                </div>
                <div class="row">
                    <div class="col-xs-7">
                    </div>
                    <div class="col-xs-2 text-right" style="height: 20px;">Print Time:</div>
                    <div class="col-xs-3 text-left" style="height: 20px;"><t t-datetime="%Y-%m-%d %H:%M"/></div>
                </div>') where type='qweb' and key like 'all_form_design.report_x_af_%';

insert into ir_translation (lang, src, value, res_id, module, name, type) 
select 'zh_CN', 'Signature:', '签字：', id, 'all_form_design', 'ir.ui.view,arch_db', 'model' 
from ir_ui_view where type='qweb' and key like 'all_form_design.report_x_af_%';

insert into ir_translation (lang, src, value, res_id, module, name, type) 
select 'zh_CN', 'Print Time:', '打印时间：', id, 'all_form_design', 'ir.ui.view,arch_db', 'model' 
from ir_ui_view where type='qweb' and key like 'all_form_design.report_x_af_%';

-- 可复制选项
update ir_model_fields set copy='t' where model like 'x_af_%' and 
name not in ('id', 'create_date', 'create_uid', 'write_date', 'write_uid');

-- 撤回的历史数据
update ir_ui_view set arch_db=replace(arch_db, '<field name="can_submit" invisible="1"/>', 
'<field name="can_submit" invisible="1"/>
<field name="can_recall" invisible="1"/>') where model like 'x_af_%' and type='form';

update ir_ui_view set arch_db=replace(arch_db, '<button name="do_rollback" string="Rollback" type="object" attrs="{''invisible'':[(''can_rollback'',''='',False)]}" class="oe_highlight"/>', 
'<button name="do_rollback" string="Rollback" type="object" attrs="{''invisible'':[(''can_rollback'',''='',False)]}" class="oe_highlight"/>
<button name="do_recall" string="Recall" type="object" attrs="{''invisible'': [(''can_recall'', ''='', False)]}" class="oe_highlight" confirm="Confirm Cancel"/>') where model like 'x_af_%' and type='form';

-- 确定撤回翻译
INSERT INTO ir_translation (lang, src, name, res_id, value, state, type, module) 
SELECT 'zh_CN', 'Recall', 'ir.ui.view,arch_db', v.id, '撤回', 'translated', 'model', 'all_form_design'
FROM ir_ui_view v WHERE model LIKE 'x_af_%' AND type='form' ORDER BY model ASC;

INSERT INTO ir_translation (lang, src, name, res_id, value, state, type, module) 
SELECT 'zh_CN', 'Confirm Cancel', 'ir.ui.view,arch_db', v.id, '确定撤回', 'translated', 'model', 'all_form_design'
FROM ir_ui_view v WHERE model LIKE 'x_af_%' AND type='form' ORDER BY model ASC;

查询：
select value from ir_translation WHERE lang='en_US' and module='hr_base' and res_id=(SELECT id FROM ir_model_fields WHERE name='bank_name' and model='hr.employee');


-- 删除画面多余 filed
DELETE FROM ir_ui_view WHERE model_data_id in (SELECT id FROM ir_model_data WHERE module='hr_cost_center' AND model='ir.ui.view' AND name in ('view_hr_employee_cost_center_form', 'view_hr_department_cost_center_form', 'view_job_transfer_cost_center_form', 'view_rank_job_transfer_cost_center_form'));

DELETE FROM ir_model_data WHERE module='hr_cost_center' AND model='ir.ui.view' AND name in ('view_hr_employee_cost_center_form', 'view_hr_department_cost_center_form', 'view_job_transfer_cost_center_form', 'view_rank_job_transfer_cost_center_form');


-- 查询结果作为值插入：
INSERT INTO import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) 
SELECT true, 'many2one', false, 23 , true, i1.id, i2.id, i3.id 
	FROM ir_model_fields i1, ir_model_fields i2, import_excel i3 
WHERE i1.model='hr.employee' AND i1.name='employee_type_rep' AND i2.model='hr.employee.type' AND i2.name='name' AND i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true , 'many2one', false, 23 , true , i1.id , i2.id , i3.id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';

insert into import_fields (unique_index, field_type, create_if_not_find, sequence, required, field_id, relation_field, import_model_id) select true as unique_index, 'many2one' as field_type, false as create_if_not_find, 23 as sequence , true as required, i1.id as field_id, i2.id as relation_field, i3.id as import_model_id from ir_model_fields i1, ir_model_fields i2, import_excel i3 where i1.model='hr.employee' AND i1.name='employee_type_rep' and i2.model='hr.employee.type' AND i2.name='name' and i3.name='基本信息';


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

insert into ir_translation (lang, src, name, res_id, module, state, value, type, is_customer)
select 'zh_CN', 'Education Background1', 'ir.ui.view,arch_db', i1.id, 'hr_career', 'translated', '员工学历信息1', 'model', TRUE
from ir_ui_view i1 where model='hr.employee' and name='hr.employee.career.view.form';


CREATE OR REPLACE FUNCTION dropNull(varchar) RETURNS integer AS $$
DECLARE
  columnName varchar(50);
BEGIN

    FOR columnName IN

select a.attname
  from pg_catalog.pg_attribute a
 where attrelid = $1::regclass
   and a.attnum > 0
   and not a.attisdropped
   and a.attnotnull and a.attname not in(

   SELECT
  pg_attribute.attname
FROM pg_index, pg_class, pg_attribute
WHERE
  pg_class.oid = $1::regclass AND
  indrelid = pg_class.oid AND
  pg_attribute.attrelid = pg_class.oid AND
  pg_attribute.attnum = any(pg_index.indkey)
  AND indisprimary)

          LOOP
          EXECUTE 'ALTER TABLE ' || $1 ||' ALTER COLUMN '||columnName||' DROP NOT NULL';
        END LOOP;
    RAISE NOTICE 'Done removing the NOT NULL Constraints for TABLE: %', $1;
    RETURN 1;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE model varchar;
BEGIN
FOR model IN (select design_model from all_form_design)
LOOP
  PERFORM dropNull(model);
END LOOP;
END $$;

