# -*- coding: utf-8 -*-

import openerp.http as oewebhttp
import logging
_logger = logging.getLogger(__name__)


class PersonnelEventMJsonWebClient(oewebhttp.Controller):
    """
    APP 端人事事件审批接口
    """

    # @oewebhttp.route('/mjson/personnel_event', type='json', auth="none", csrf=False)
    @oewebhttp.route('/mjson/personnel_event', type='json', auth="user")
    def app_personnel_event(self, req, *arg, **kwargs):
        """
        __description: APP 端人事事件审批
        """

        result = PersonnelEventController.get_json_content(req)
        if result:
            return result
        else:
            return {'code': 3, 'msg': 'error'}


class PersonnelEventController(object):
    """
    __description: APP 端人事事件审批
    """

    # k: event_type, v: model_name
    model = {
        'probation': 'employee.probation',
        'rank_job': 'rank.job.transfer',
        'job': 'job.transfer',
        'employee_rank': 'employee.rank.adjust',
        'dimission': 'employee.dimission',
        'termination': 'hr.termination',
        'contract': 'hr.contract',
        'salary': 'single.salary.adjustment',
    }

    # k: action, v: method_name
    method = {
        'query': 'app_view_detail',
        'approve': 'app_do_approved',
        'reject': 'app_do_reject',
        'cancel': 'app_do_cancel',
        'save': 'app_do_update',
    }

    lang = {
        'en': 'en_US',
        'zh': 'zh_CN',
    }

    @classmethod
    def get_json_content(cls, req):
        """
        __description: APP 端人事事件审批统一入口，直接可以获取 json 字符串

        :param req: JsonRequest
            参数包括：
            event_type: 事件类型，包括以下几种：
                员工转正
                岗位职级调整
                岗位调动
                职级调整
                员工离职
                hr 申请离职
                合同、合同续签
                薪资调整
            id：event_type 对应的 record_id
            action：event_type 的动作，查看详情，审批，保存
            description: 备注
        :return: json 字符串
        """

        cr = req.cr
        uid = req.session.uid
        kwargs = req.params

        if 'id' in kwargs and 'event_type' in kwargs and 'action' in kwargs:
            ids = [kwargs['id']]
            context = req.session.get_context().copy()
            language = req.identication.get('language', False)
            if language and language in cls.lang:
                context['lang'] = cls.lang[language]
            context.update({'suspend_security': True})

            event_type = kwargs['event_type']
            action = kwargs['action']

            if event_type in cls.model and action in cls.method:
                if 'comment' in kwargs:
                    context.update({'comment': kwargs['comment']})
                if 'description' in kwargs:
                    context.update({'description': kwargs['description']})

                result = getattr(req.registry.get(cls.model[event_type]), cls.method[action])(cr, uid, ids, context)
            else:
                result = {'code': 1, 'msg': 'key error'}
        else:
            result = {'code': 2, 'msg': 'key not exist'}

        return result
