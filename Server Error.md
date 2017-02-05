Server Error

Traceback (most recent call last):
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/controllers/main.py", line 101, in report_download
    response = self.report_routes(reportname, docids=docids, converter='pdf')
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/http.py", line 509, in response_wrap
    response = f(*args, **kw)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/controllers/main.py", line 45, in report_routes
    pdf = report_obj.get_pdf(cr, uid, docids, reportname, data=data, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/common_addons/addons/eroad_printer_center/report.py", line 222, in get_pdf
    context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/models/report.py", line 156, in get_pdf
    html = self.get_html(cr, uid, ids, report_name, data=data, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/models/report.py", line 120, in get_html
    return particularreport_obj.render_html(cr, uid, ids, data=data, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/models/abstract_report.py", line 48, in render_html
    return self.pool['report'].render(cr, uid, [], self._template, docargs, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/report/models/report.py", line 106, in render
    return view_obj.render(cr, uid, template, values, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/addons/web_editor/models/ir_ui_view.py", line 29, in render
    return super(view, self).render(cr, uid, id_or_xml_id, values=values, engine=engine, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_ui_view.py", line 1070, in render
    return self.pool[engine].render(cr, uid, id_or_xml_id, qcontext, loader=loader, context=context)
  File "/Users/zhenglong/proj/zhengl/./odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 254, in render
    return self.render_node(element, qwebcontext, generated_attributes=qwebcontext.pop('generated_attributes', ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 297, in render_node
    result = self.render_element(element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 295, in render_node
    result = self._render_tag[t_render](self, element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 448, in render_tag_call
    d[0] = self.render_element(element, template_attributes, generated_attributes, d)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 295, in render_node
    result = self._render_tag[t_render](self, element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 426, in render_tag_foreach
    ru.append(self.render_element(element, template_attributes, generated_attributes, copy_qwebcontext))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 297, in render_node
    result = self.render_element(element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 297, in render_node
    result = self.render_element(element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 297, in render_node
    result = self.render_element(element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 297, in render_node
    result = self.render_element(element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 325, in render_element
    raise_qweb_exception(message="Could not render element %r" % element.tag, node=element, template=template)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 320, in render_element
    generated_attributes= name == "t" and generated_attributes or ''))
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 295, in render_node
    result = self._render_tag[t_render](self, element, template_attributes, generated_attributes, qwebcontext)
  File "/Users/zhenglong/proj/zhengl/odoo/openerp/addons/base/ir/ir_qweb.py", line 503, in render_tag_field
    field = record._fields[field_name]
QWebException: 'employee_name'