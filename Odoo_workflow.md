# 工作流

查到相对应的工作流  设置->工作流->工作流
对应的模型 workflow  对应的表格 是 wkf 开头的表

一个工作流模型在Session模型上都加入了state字段 ；有三种字段， Draft Confirmed Done
有效的转变有：
Draft ->Confirmed 
Confirmed -> Draft
Confirmed -> Done
Done -> Draft

工作流中的节点叫 “活动(activity)” 弧线连接叫“转变(transition)”
转变可以增加属性如 条件、信号、触发器

### 工作流功效：

* 关于记录如何演变的描述
* 根据多样的弹性的条件建立自动化行动机制
* 管理公司流程和确认规则
* 管理对象间的互动
* 在他们的生命期内一个可视化的流程图

### 定义工作流对象：
addons/hr_holidays/hr_holidayss_workflow.xml:

```xml
<record model="workflow" id="wkf_holidays">
    <field name="name">hr.wkf.holidays</field>
    <field name="osv">hr.holidays</field>
    <field name="on_create">True</field>
</record>
```

* model：固定取值"workflow"
* id：任意值，唯一标识本工作流
* name: 本工作流的名称，随意
* osv: 这个很重要，对应的具体的那个模型
* on_create: 一般设置为True, 工作流会根据每一个模型新建一个对象再实例化一次

### 工作流和工作流实例：
工作流定义了对某一类型的对象，如采购订单（PO）的处理流程。
例如，PO单的一般处理流程也许是：
1）新建PO，State = draft；
2）审批PO，审批的同时，
  a)系统自动产生收货单，工仓库收货；
  b)系统自动产生凭据（Invoice），供财务确认付款；
  c)系统自动产生PDF的采购订单，并自动EMail给该PO单对应的供应商。

但对于特定的某个PO对象，需要一个工作流实例，以记录本PO对象处在流程的哪个阶段，
   如PO1尚在draft状态，PO2已经审批通过。PO单的审批，以及对应的a)、b)、c)的动作，
   都可以在OE的工作流中定义解决，而不需要全编码在PO对象上。
   即工作流实现了流程处理相关的代码和被处理对象的代码相分离，降低了不同处理代码的耦合性，
   增加了系统功能的柔软性。

### 创建活动(Activity)：

```xml
<record model="workflow.activity" id="activity_id">
    <field name="wkf_id" ref="workflow_id"/>
    <field name="name">activity.name</field>
    <field name="kind">dummy | function | subflow | stopall</field>
    <field name="subflow_id">subflow_id</field>
    <field name="action">(...)</field>
    <field name="action_id">(...)</field>
    <field name="split_mode">XOR | OR | AND</field>
    <field name="join_mode">XOR | AND</field>
    <field name="signal_send">(...)</field>
    <field name="flow_start">True | False</field>
    <field name="flow_stop">True | False</field>
</record>
```

* wkt_id: 属于某个工作流对象, 我们看到这里的 ref 语法如果是引用本模型内的对象则可以省略
* model：**固定取值workflow.activity**
* kind: 有四种 dummy, function, subflow, stopall
  **dummy** 表示不执行任何动作，即action中定义的代码不会被执行;
  **function** 表示执行action中定义的python代码，且执行action_id中定义的server action。常见情况是，action中定义一个write方法，修改流程关联的对象的状态。对于Function类型的节点，action中定义的代码或者返回False，或者返回一个客户端动作id（A client action should be returned）;
  **subflow** 类型表示触发“subflow_id”中指定的工作流。仔细的读者或许要问，工作流的执行总是和某个被处理的对象关联，是的，如果定义了action.subflow 关联的对象id 由action中定义的代码返回。如果没有定义action，系统默认subflow关联的对象和本节点所属的工作流处理的对象id一致;
  **stopall** 类型表示，流程到此节点则结束，但结束前，系统仍会执行action中的代码。
* subflow_id: 表示，触发子工作流subflow_id，在该**子工作流**中，通常**必须定义****signal_send**，
* signal_send: 定义父流程中的某个signal，表示，**子流程处理结束后触发父流程中的信号subflow.signal**。注意，用于**父子流程通信的工作流signal必须是形如subflow.*** 。执行完本节点的动作（action及action_id定义的动作）后，应向别的工作流发往的signal，格式是：subflow.signal。**subflow_id和signal_send必须配合使用**

例如，在HR模块的workflow "wkf_expenses"中，需要开发票时候，它触发流程account模块中的工作流“account.wkf”（ <field name="subflow_id" ref="account.wkf"/>）。
account.wkf处理完成后，发出信号subflow.paid 通知wkf_expenses流程（<field name="signal_send">subflow.paid</field>）。
wkf_expenses中定义了信号subflow.paid（<field name="signal">subflow.paid</field>）。   


* split_mode：有三个选项，XOR，OR，AND，默认是XOR。**XOR** 表示，由本节点始发的出迁移中，沿着第一个满足迁移条件的**迁移跳转**。**OR** 表示由本节点始发的出迁移中，只要满足迁移条件即沿该迁移跳转。**AND** 表示由本节点始发的出迁移中，只有所有迁移皆满足迁移条件才跳转，而且是同时沿所有迁移跳转。XOR 只有一个跳转，OR 有零或多个跳转，AND 有零或全部跳转。     
* join_mode：有两个选项，XOR，AND，默认是XOR。XOR 表示，以本节点为终点的入迁移中，只要有一个跳至本节点，即执行本节点的action。AND 表示，以本节点为终点的入迁移中，只有所有迁移都已经跳至本节点，才执行本节点的action。action 具体的动作（于模型上）
* flow_start：表示流程的开始节点, 如果设置为 **True 工作流会从这里开始**
* flow_stop: 一个工作流的完成就是所有的活动有 flow_stop 属性的都设置为了 True

```xml
如：创建请假条：
<record model="workflow.activity" id="act_draft"> <!-- draft -->
    <field name="wkf_id" ref="wkf_holidays" />
    <field name="name">draft</field>
    <field name="flow_start" eval="False"/>
    <field name="kind">function</field>
    <field name="action">holidays_reset()</field>
</record>

确认请假条：
<record model="workflow.activity" id="act_confirm"> <!-- submitted -->
    <field name="wkf_id" ref="wkf_holidays" />
    <field name="name">confirm</field>
    <field name="flow_start" eval="True"/>
    <field name="kind">function</field>
    <field name="action">holidays_confirm()</field>
    <field name="split_mode">OR</field>
</record>
```

### 创建迁移(Transition)：

```xml
<record model=”workflow.transition” id=”holiday_draft2confirm”> 
    <!-- 1. draft->submitted (confirm signal) -->
    <field name=”act_from” ref=”act_draft” />
    <field name=”act_to” ref=”act_confirm” />
    <field name=”signal”>confirm</field>
    <field name=”condition”>can_reset</field>
    <field name=”group_id” ref=”base.group_user”/>
</record>
```

转变对象属于 workflow.transition 模型。

* act_from：本迁移的**起始**节点，引用之前定义的Activity。
* act_to：本迁移的**结束**节点，引用之前定义的Activity。
* signal：**触发本迁移的信号**，表示，如果系统收到signal定义的信号，则触发本迁移。触发信号有三种方式，
1. 最常见的是用户**点击视图中的“name = 本处定义的signal”的button**，此时相当于**向系统发送迁移信号量**。系统会根据视图中的对象id，找到对象关联的workflow，再找到如果设置为 **True 工作流会从这里开始**，触发之。
2. 调用**workflow_service**的方法：trg_validate(self, uid, res_type, res_id, signal, cr)，此方法表示，触发对象类型res_type关联的workflow的signal信号，工作流实例关联的对象实例是 res_id。
3. 子流程的**signal_send** 发出的信号，此种情况前文已说过。
* condition：迁移的条件，是一段Python代码，通常是一个**函数调用**。当系统**收到signal中定义的信号时候**，检查此处的条件，**条件为真则实际触发迁移**。
* trigger_model和trigger_expr_id：此二字段表示启动一个新工作流实例。trigger_model定义对象类型，trigger_expr_id 定义一段Python代码，返回trigger_model类型的对象id。此二字段表示，如果act_from 中的action 执行完毕，且condition 条件OK，则系统中插入一个trigger_model类型，
  trigger_expr_id返回的对象id关联的工作流实例。然后，可以调用workflow_service的方法trg_trigger(self, uid, res_type, res_id, cr)实际执行该工作流。
  实际使用例子请参考Sale模块的工作流定义 wkf_sale：

```xml
<field name="trigger_model">procurement.order</field>
<field name="trigger_expr_id">procurement_lines_get()</field>
```

* group_id 权限组 如 <field name="group_id" ref="groupid" />

  ​

1. 查询某个工作流的activity和transition

select 

a.name,a.osv,a.on_create, d.id,d.condition,d.group_id,d.signal,b.id as from_act_id,b.name as from_action,b.split_mode,b.join_mode,b.kind,c.id as to_act_id,c.name as to_action,c.split_mode,c.join_mode,c.kind

from wkf a
join wkf_activity b on a.id = b.wkf_id
join wkf_activity c on a.id = c.wkf_id
join wkf_transition d on b.id = d.act_from and c.id = d.act_to
where a.osv = 'sale.order'
and b.name in('sent' ,'router', 'wait_invoice','wait_ship','ship')
order by b.name

2. 查询某个对象的工作流实例的workitem

select a.inst_id,a.act_id,c.name as act_name,a.state, c.split_mode,c.join_mode,c.kind
from wkf_workitem a
join wkf_instance b on a.inst_id = b.id
join wkf_activity c on a.act_id = c.id
where b.res_type = 'sale.order'
and b.res_id = 53

3. 查询某个对象的工作流实例的log

select a.* ,b.name as act_name
from wkf_logs a
join wkf_activity b on a.act_id = b.id
where res_id = 53 and res_type = 'sale.order'

### 来一个完整的工作流文件 

```xml
<?xml version=”1.0” ?>
<openerp>
    <data noupdate=”0”>
        <record id=”wkf_qingjia” model=”workflow” >
            <field name=”name”>wkf.qingjia</field>
            <field name=”osv”>qingjia.qingjd</field>
            <field name=”on_create”>True</field>
        </record>
        <record id=”act_draft” model=”workflow.activity” >
            <field name=”wkf_id” ref=”wkf_qingjia” />
            <field name=”name”>draft</field>
            <field name=”flow_start” eval=”True”/>
            <field name=”kind”>function</field>
            <field name=”action”>draft()</field>
        </record>
        <record id=”act_confirm” model=”workflow.activity” >
            <field name=”wkf_id” ref=”wkf_qingjia” />
            <field name=”name”>confirm</field>
            <field name=”kind”>function</field>
            <field name=”action”>confirm()</field>
        </record>
        <record id=”act_accept” model=”workflow.activity” >
            <field name=”wkf_id” ref=”wkf_qingjia” />
            <field name=”name”>accept</field>
            <field name=”kind”>function</field>
            <field name=”flow_stop”>True</field>
            <field name=”action”>accept()</field>
        </record>
        <record id=”act_reject” model=”workflow.activity” >
            <field name=”wkf_id” ref=”wkf_qingjia” />
            <field name=”name”>reject</field>
            <field name=”kind”>function</field>
            <field name=”action”>reject()</field>
        </record>
        <record model=”workflow.transition” id=”qingjia_draft2confirm”>
            <field name=”act_from” ref=”act_draft” />
            <field name=”act_to” ref=”act_confirm” />
            <field name=”signal”>btn_confirm</field>
        </record>
        <record model=”workflow.transition” id=”qingjia_confirm2accept”>
            <field name=”act_from” ref=”act_confirm” />
            <field name=”act_to” ref=”act_accept” />
            <field name=”signal”>btn_accept</field>
            <field name=”condition”>is_manager</field>
        </record>
        <record model=”workflow.transition” id=”qingjia_confirm2reject”>
            <field name=”act_from” ref=”act_confirm” />
            <field name=”act_to” ref=”act_reject” />
            <field name=”signal”>btn_reject</field>
            <field name=”condition”>is_manager</field>
        </record>
    </data>
</openerp>
```

### 对应的模型支持

```python
from openerp import models, fields, api
import logging

class Qingjd(models.Model):
    _name = ’qingjia.qingjd’
    name = fields.Many2one(’hr.employee’, string=” 申请人”, readonly=True)
    manager = fields.Many2one(’hr.employee’, string=” 主管”,readonly=True)
    beginning = fields.Datetime(string=” 开始时间”, required=True,
    default = fields.Datetime.now())
    ending = fields.Datetime(string=” 结束时间”, required=True)
    reason = fields.Text(string=” 请假事由”,required=True)
    accept_reason = fields.Text(string=” 同意理由”,default=” 同意。 ”)
    #########compute 没有写入数据库 on the fly 可以被 workflow 的 condition 调用
    current_name = fields.Many2one(’hr.employee’, string=” 当前登录人”,compute=”_get_current_name”)
    is_manager = fields.Boolean(compute=’_get_is_manager’)
    ######
    state = fields.Selection([
        (’draft’, ” 草稿”),
        (’confirmed’, ’ 待审核’),
        (’accepted’, ’ 批准’),
        (’rejected’, ’ 拒绝’),
        ],string=’ 状态’,default=’draft’,readonly=True)
        
    @api.model# 使用新的 api
    def _get_default_name(self):
        uid = self.env.uid
        res = self.env[’resource.resource’].search([(’user_id’,’=’,uid)])
        name = res.name
        employee = self.env[’hr.employee’].search(
                [(’name_related’,’=’,name)])
        # for i in self.env.user:# 说明其是 recordset
        # print(’hello’)
        return employee
        
    @api.model
    def _get_default_manager(self):# 单记录 recordset 可以直接用点记号读取属性值
        uid = self.env.uid
        res = self.env[’resource.resource’].search([(’user_id’,’=’,uid)])
        name = res.name
        employee = self.env[’hr.employee’].search(
            [(’name_related’,’=’,name)])
        logging.info(”myinfo {}”.format(employee.parent_id))
        return employee.parent_id # 似乎有这种数字引用方法值得我们注意
        _defaults = {
            ’name’ : _get_default_name ,
            ’manager’ : _get_default_manager ,
            }
            
    def _get_is_manager(self):### 这里 return 不起作用
        print(’----------test’)
        print(self.current_name, self.manager,self.env.uid)
        if self.current_name == self.manager:
            self.is_manager = True
        else:
            self.is_manager = False
            
    def _get_current_name(self):
        uid = self.env.uid
        res = self.env[’resource.resource’].search([(’user_id’,’=’,uid)])
        name = res.name
        employee = self.env[’hr.employee’].search(
        [(’name_related’,’=’,name)])
        self.current_name = employee

    def draft(self, cr, uid, ids, context=None):
        if context is None:
        context={}
        self.write(cr,uid,ids,{’state’:’draft’},context=context)
        return True
        
    def confirm(self, cr, uid, ids, context=None):
        if context is None:
            context={}
            self.write(cr,uid,ids,{’state’:’confirmed’},context=context)
        return True
        
    def accept(self, cr, uid, ids, context=None):
        if context is None:
            context={}
            self.write(cr,uid,ids,{’state’:’accepted’},context=context)
            print(’ 你的请假单被批准了’)
        return True
        
    def reject(self, cr, uid, ids, context=None):
        if context is None:
            context={}
            self.write(cr,uid,ids,{’state’:’rejected’},context=context)
            print(’ 抱歉，你的请假单没有被批准。 ’)
        return True    
```

### 对应的视图支持

```xml
<?xml version=”1.0”?>
<openerp>
    <data>
    <!--
    打开请假单动作
    -->
    <act_window id=”action_qingjia_qingjd”
        name=” 请假单”
        res_model=”qingjia.qingjd”
        view_mode=”tree,form” />
    <!--
    表单视图
    -->
    <record id=”qingjia_qingjd_form” model=”ir.ui.view”>
        <field name=”name”>qing jia dan form</field>
        <field name=”model”>qingjia.qingjd</field>
        <field name=”arch” type=”xml”>
    <form>
    <!--button 的name值就是工作流迁移的信号名称-->
    <header>
        <button name=”btn_confirm” type=”workflow” states=”draft”
            string=” 发送” class=”oe_highlight” />
        <button name=”btn_accept” type=”workflow” states=”confirmed”
            string=” 批准” class=”oe_highlight”/>
        <button name=”btn_reject” type=”workflow” states=”confirmed”
            string=” 拒绝” class=”oe_highlight”/>
        <field name=”state” widget=”statusbar” statusbar_visible=”draft,confirmed,accepted,rejected” class=”oe_highlight” type=”workflow”/>
    </header>
    
    <sheet>
        <group name=”group_top” string=” 请假单”>
            <group name=”group_left”>
            <field name=”name”/>
            <field name=”beginning”/>
            </group>
            <group name=”group_right”>
            <field name=”manager”/>
            <field name=”ending”/>
            </group>
        </group>
        
        <group name=”group_below”>
        <field name=”reason”/>
        </group>
    </sheet>
    </form>
    </field>
    </record>
    <!--
    tree 视图
    -->
    <record id=”qingjia_qingjd_tree” model=”ir.ui.view”>
    <field name=”name”>qing jia dan tree</field>
    <field name=”model”>qingjia.qingjd</field>
    <field name=”arch” type=”xml”>
        <tree>
            <field name=”name”/>
            <field name=”beginning”/>
            <field name=”ending”/>
            <field name=”state”/>
        </tree>
    </field>
    </record>
    <!--
    加入菜单
    -->
    <menuitem id=”menu_qingjia” name=” 请假” sequence=”0”></menuitem>
    <menuitem id=”menu_qingjia_qingjiadan” name=” 请假单” parent=”menu_qingjia”></menuitem>
    <menuitem id=”menu_qingjia_qingjiadan_qingjiadan” parent=”menu_qingjia_qingjiadan” action=”action_qingjia_qingjd”></menuitem>
    </data>
</openerp>
```


# 权限


OpenERP 中的预设组,在每个模块下的 **security** 目录下的文件:**xxx_security.xml、ir.model.access.csv**
定义。其中_security.xml 文件**定义组**和**组对菜单**的访问权限,ir.model.access.csv **定义组对对象的权限矩阵**。



​			
​		
​	
