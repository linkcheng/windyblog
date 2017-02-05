# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from openerp import models, api, _, fields
from openerp.models import BaseModel
from openerp.exceptions import UserError
from operator import itemgetter


class TerminationController(models.AbstractModel):
    _name = 'termination.controller'
    _inherit = ['termination.model', 'ir.needaction_mixin', 'personnel.detail']
    _description = "Termination Controller"

    @api.multi
    def push_remind(self, title, message, user_ids, action, title_args=(), message_args=()):
        for record in self:
            msg = {
                'record_id': record.id,
                'model_name': record._name,
                'type': 'personnel_detail',
                'action': action,
            }
            lang_user_ids_dict = self.env['res.users'].get_res_partner_lang(user_ids)

            for lang, user_id_list in lang_user_ids_dict.items():
                title_with_lang = self.env['ir.translation'].format_the_string_with_lang(title, title_args, lang)
                message_with_lang = self.env['ir.translation'].format_the_string_with_lang(message, message_args, lang)
                msg.update({
                    'title': title_with_lang,
                    'message': message_with_lang,
                })
                self.env['app.action'].jpush_send(msg, user_ids=user_id_list, push_type='double')

        return True

    @api.multi
    def app_view_detail(self):
        res = dict()
        head = super(TerminationController, self).app_view_detail()
        res.update(head)

        for record in self:
            # 构建各自的 json content dict
            data = {
                "approver_ids": [user.id for user in record.approver_ids],
                "content": [
                    {
                        "type": "date",
                        "can_edit": True,
                        "title": self.get_translation('Termination Date'),
                        "value": record.leave_time,
                        "key": "leave_time",
                    },
                    {
                        "type": "text",
                        "can_edit": False,
                        "title": self.get_translation('Remarks'),
                        "value": record.leave_reason or '',
                        "key": "leave_reason",
                    },
                ],
            }

        if 'approve_state' in res and 'can_cancel' in res['approve_state']:
            res['approve_state']['can_cancel'] = False  # 后端没有实现撤回功能，所以暂时不能撤回

        res.update(data)
        return res

    @api.multi
    def app_do_reject(self):
        if 'description' in self.env.context:
            vals = self.env.context['description']

            for k, v in vals.items():
                if v == '':   # date 类型置空不能用''，用 False
                    vals[k] = False

            r = self.write(vals)
        res = super(TerminationController, self).app_do_reject()
        return res

    @api.multi
    def app_do_approved(self):
        if 'description' in self.env.context:
            vals = self.env.context['description']

            for k, v in vals.items():
                if v == '':
                    vals[k] = False

            r = self.write(vals)
        res = super(TerminationController, self).app_do_approved()
        return res



class HrTermination(models.Model):
    _name = 'hr.termination'
    _description = "HR Termination"
    _inherit = ['termination.controller', 'work.bench']
    _order = "create_date desc"

    _workbench_search = {
        'remark': lambda self: self.get_translation(self._description, 'ir.model,name') or '',
        'title': lambda self: self.employee_name,
        'description': '',
        'record_id': lambda self: self.id,
        'date': lambda self: self.leave_time,
        'type': 'personnel_detail',
        'color': '#3fa2a3',
        'state': lambda self:
        self.env['ir.translation'].selection_field_key_translations_map('approve.instance', 'state', lang=self._context['lang'])[
            getattr(self, 'state')]
    }

    def _search_app_action(self, search_place):
        return 'eHR://personalEvent?id=%d&event_type=termination' % self.id

    name = fields.Char(string='ID', readonly=True, states={'draft': [('readonly', False)]}, required=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code(self._name))

    # 与审批流有关，view 中 domain 使用
    approver_ids = fields.Many2many('res.users', 'hr_termination_approver_rel', 'termination_id', 'user_id', string='Approver')
    approved_ids = fields.Many2many('res.users', 'hr_termination_approved_rel', 'termination_id', 'user_id', string='Approved by')

    @api.multi
    def build_approve_remind(self, msg, approver_ids):
        """
        构建审批人的推送消息
        :return:
        """
        if not isinstance(approver_ids, (list, tuple)):
            approver_ids = [approver_ids]

        title = _('Personnel Event Approval')
        action_push = 'eHR://personalEvent?id=%d&event_type=termination' % self.id

        msg_args_list = [
            {
                'src_or_value': self.create_uid.partner_id.name,
                'need_translate': False,
            },
            {
                'src_or_value': self._description,
                'translate_name': 'ir.model,name',
                'translate_type': 'model',
                'need_translate': True,
            }
        ]

        # 推送消息
        self.push_remind(title, msg, approver_ids, action_push, message_args=msg_args_list)

    @api.multi
    def build_create_remind(self, msg, push_uid):
        """
        构建创建者的推送消息
        :return:
        """
        if not isinstance(push_uid, (list, tuple)):
            push_uid = [push_uid]

        title = _('Personnel Event Approval')
        action_push = 'eHR://personalEvent?id=%d&event_type=termination' % self.id

        msg_args_list = [
            {
                'src_or_value': self._description,
                'translate_name': 'ir.model,name',
                'translate_type': 'model',
                'need_translate': True,
            }
        ]

        # 推送消息
        self.push_remind(title, msg, push_uid, action_push, message_args=msg_args_list)
