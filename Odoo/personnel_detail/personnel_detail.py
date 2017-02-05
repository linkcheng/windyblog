# -*- coding: utf-8 -*-

from openerp import models, api, _
from openerp import fields


class PersonnelDetail(models.AbstractModel):
    """
    人事事件详情
    包括人事事件公共字段，以及 APP 端操作所需接口和审批流触发的函数

    各人事事件需要重载以下方法：
    def get_translation(self, src, translate_type='ir.model.fields,field_description'):  # 根据语言获取 src 的翻译值
    def build_approve_remind(self, msg, approver_ids):  # 给审批者推送的消息格式
    def build_create_remind(self, msg, push_uid):  # 给创建者推送的消息格式

    各人事事件根据具体业务重写以下发法：
    def app_view_detail(self):  # 返回 APP 端详情展示页面信息
    def app_do_approved(self):  # APP 端审批批准所触发函数
    def app_do_reject(self):  # APP 端审批拒绝所触发函数
    def app_do_cancel(self):  # APP 端撤回所触发函数
    def app_do_update(self):  # APP 端更信息所触发函数

    """

    _name = 'personnel.detail'
    _inherit = ['approve.instance']
    _description = 'Personnel Detail'

    name = fields.Char(string='ID', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')

    employee_number = fields.Char(string='Employee Number', related='employee_id.employee_number', update=['draft'], store=True)
    employee_name = fields.Char(string='Employee Name', related="employee_id.name", update=['draft'], store=True)
    department_id = fields.Many2one('hr.department', string='Org Unit', related='employee_id.department_id', update=['draft'], store=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_id.job_id', update=['draft'], store=True)
    parent_id = fields.Many2one('hr.employee', string='Supervisor', related='employee_id.parent_id', update=['draft'], store=True)
    dep_manager = fields.Many2one('hr.employee', string='Org Unit Manager', related='department_id.manager_id', update=['draft'], store=True)
    # 职级
    now_rank = fields.Many2one('employee.rank', string='Job Grade', related="employee_id.employee_now_rank", update=['draft'], store=True)
    # 职级类型
    now_grade = fields.Many2one('employee.grade', string='Job Grade Category', related='now_rank.grade_type_id', update=['draft'], store=True)
    # 职能
    function_id = fields.Many2one('hr.function', string='Function', related='employee_id.function_id', update=['draft'], store=True)
    # 员工组
    employee_group_rep = fields.Many2one('hr.employee.group', string='Employee Group', related='employee_id.employee_group_rep', update=['draft'], store=True)
    # 入职日期
    hiredate = fields.Date(string='Hire Date', related='employee_id.hiredate', update=['draft'], store=True)
    # 联系电话
    work_phone = fields.Char(string='Phone Number', related='employee_id.work_phone', update=['draft'], store=True)
    # 成本中心
    cost_center = fields.Many2one('cost.center', string='Cost Center', related='employee_id.cost_center', update=['draft'], store=True)

    @api.model
    def get_translation(self, src, translate_type='ir.model.fields,field_description', module=None):
        """
        @param src: 需要翻译的原术语
        @param translate_type: 原术语类型，默认为模型字段类型
        @param module: 模块名
        @return:
        """

        lang = self.env.lang
        module = module or self._module

        self.env.cr.execute("SELECT value FROM ir_translation WHERE module=%s AND lang=%s AND src=%s AND name=%s",
                            (module, lang, src, translate_type))
        res_trans = self.env.cr.fetchone()
        res = res_trans and res_trans[0] or src

        return res

    @api.multi
    def build_approve_remind(self, title, msg, approver_ids):
        """
        构建审批人的推送消息
        :return:
        """
        pass

    @api.multi
    def build_create_remind(self, title, msg, push_uid):
        """
        构建创建者的推送消息
        :return:
        """
        pass

    @api.multi
    def app_view_detail(self):
        """
        APP 端详情展示页面信息
        :return:
        """
        data = dict()
        state_dic = self.env['ir.translation'].selection_field_key_translations_map('approve.instance', 'state', lang=self._context['lang'])

        for record in self:
            data = {
                "state": record.state,
                "state_for_show": state_dic[record.state] if record.state in state_dic else record.state,
                "title": self.get_translation(record._description, 'ir.model,name'),
                "id": record.id,
                "serial_number": record.name,
                "create_uid": record.create_uid.id,
                "name": record.employee_name,
                "show_pdf": False,
            }

            # 职级 值显示成【职级类别-职级】
            employee_now_rank = ''
            if record.now_grade.name:
                employee_now_rank = record.now_grade.name
            if record.now_rank.name:
                if employee_now_rank:
                    employee_now_rank = employee_now_rank + '-' + record.now_rank.name
                else:
                    employee_now_rank = record.now_rank.name

            emp_detail = {
                "name": record.employee_name,
                "employee_number": record.employee_number,
                "department_id": record.department_id.name,
                "job_id": record.job_id.name,
                "supervisor": record.parent_id.name,
                "org_unit_manager": record.dep_manager.name,
                "employee_now_rank": employee_now_rank,
                "function": record.function_id.name or '',
                "hire_date": record.hiredate or '',
                "work_phone": record.work_phone or '',
                "employee_group_rep": record.employee_group_rep.name or '',
                "cost_center": record.cost_center.cost_center or '',
            }

            approve_state = {
                 "can_approve": record.can_approve,
                 "can_cancel": record.can_cancel,
                 "can_rollback": record.can_rollback,
                 "can_return_draft": record.can_return_draft,
                 "approved_reason": record.activity_id.approved_reason,
                 "reject_reason": record.activity_id.reject_reason,
                 "cancel_reason": record.activity_id.cancel_reason,
                 "rollback_reason": record.activity_id.rollback_reason,
             }

            # 获取审批时间轴
            approve_notify_records = self.env['approve.notify'].search_read(
                domain=[
                    ('record_id', '=', record.id),
                    ('model', '=', self._name)
                ],
                order='approve_date desc, id desc')

            if approve_notify_records:
                notify_state_dic = self.env['ir.translation']. \
                    selection_field_key_translations_map('approve.notify', 'state', lang=self.env.context['lang'])

                comments = []
                for item in approve_notify_records:
                    job_record = self.env['hr.job'].sudo().search([('id', '=', item['job_id'][0])]) if item['job_id'] else None
                    user_record = self.env['res.users'].sudo().search([('id', '=', item['user_id'][0])]) if item['user_id'] else None

                    comments.append(
                        {
                            'comment': item['description'] if item['description'] else '',
                            'create_date': item['approve_date'] if item['approve_date'] else _('In Approval'),
                            'job_id': job_record and job_record.name or '',
                            'do_action_name': notify_state_dic[item['state']] if item['state'] in notify_state_dic else item['state'],
                            'do_action': item['state'],
                            'user_name': user_record and user_record[0].partner_id.name or '',
                        }
                    )

                data.update({'comments': comments})

            data.update({'employee_detail': emp_detail})
            data.update({'approve_state': approve_state})

        return data

    @api.multi
    def app_do_approved(self):
        """
         APP 端审批批准所触发函数
        :return:
        """
        comment = self.env.context['comment']
        self.approve_action(action='approved', msg=comment)
        return 'ok'

    @api.multi
    def app_do_reject(self):
        """
        APP 端审批拒绝所触发函数
        :return:
        """
        comment = self.env.context['comment']
        self.approve_action(action='reject', msg=comment)
        return 'ok'

    @api.multi
    def app_do_cancel(self):
        """
        APP 端撤回所触发函数
        :return:
        """
        comment = self.env.context['comment']
        self.approve_action(action='cancel', msg=comment)
        return 'ok'

    @api.multi
    def app_do_update(self):
        """
        APP 端更信息所触发函数
        :return:
        """
        pass

    @api.multi
    def app_browse_pdf(self):
        """
        APP 端 pdf 文件预览
        :return:
        """
        pass

    @api.multi
    def workflow_submit(self):
        result = super(PersonnelDetail, self).workflow_submit()
        msg = _('%s applied for a \"%s\".')
        for record in self:
            approver_ids = record.approver_ids.ids
            if approver_ids:
                self.build_approve_remind(msg, approver_ids)

        return result

    @api.multi
    def workflow_done(self):
        res = super(PersonnelDetail, self).workflow_done()
        msg = _('The \"%s\" you applied has been approved.')
        for record in self:
            push_uid = record.create_uid.id
            self.build_create_remind(msg, push_uid)

        return res

    @api.multi
    def workflow_reject(self):
        res = super(PersonnelDetail, self).workflow_reject()
        msg = _('The \"%s\" you applied has been rejected.')
        for record in self:
            push_uid = record.create_uid.id
            self.build_create_remind(msg, push_uid)

        return res

    @api.multi
    def approve_action(self, action, msg=''):
        # 审批人有审批的权限时，就能够执行拒绝、通过、撤销等操作，操作过程中不验证权限
        result = super(PersonnelDetail, self.with_context(suspend_security=True)).approve_action(action=action, msg=msg)
        msgcnt = _('%s applied for a \"%s\".')
        for record in self:
            approver_ids = record.approver_ids.ids
            if approver_ids:
                self.build_approve_remind(msgcnt, approver_ids)

        return result
