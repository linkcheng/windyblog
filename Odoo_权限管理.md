# 权限管理

### 权限管理的四个层次
* 菜单级别：不属于指定菜单所包含组的用户看不到该菜单，不客全，只是隐藏菜单，若知道菜单ID，仍然可以通过指定URL访问
* 对象级别：对某个对角是否有'创建，读取，修改，删除'的权限，可以简单理解为表对象
* 记录级别：对对象表中的数据的访问权限，比如访问“客户”对象，业务员只能对自己创建的客户有访问权限，而经理可以访问其管辖的业务员所有的“客户”对象
* 字段级别：一个对象或表上的某些字段的访问权限，比如产品的成本字段只有经理有读权限
        'name':fields.char('Name',size=128,required=True,select=True,write=['base.group_admin']
               read=['base.group_admin'])
        定义name字段只能超级用户组可读写

### 建立权限组
这是我们常说的**用户组**，会通常放在**“模块名_security.xml”**这个文件中,例如：

```xml
<record id="base.group_hr_manager" model="res.groups">
  <field name="name">Manager</field>
  <field name="comment">the user will have an access to the human resources configuration as well as statistic reports.</field>
  <field name="category_id" ref="base.module_category_human_resources"/>
  <field name="implied_ids" eval="[(4, ref('base.group_hr_user'))]"/>
  <field name="users" eval="[(4, ref('base.user_root'))]"/>
</record>

* id: 唯一标示
* model:res.groups
* name: 用户组名
* comment: 用户组的注释
* category_id: 用户组所属的模块名
* implied_ids: 基于哪个用户组，这个层级关系 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/> 是最基础的
* users: 预设用户属于这个用户组,用户名，最初是基于这个，后面一层一层递增，像上面 base.group_hr_user 定义时就是基于最基础
     

### 权限组
权限管理核心是权限组，每个权限组，可以设置权限组的 Menus, Access Right, Record Rule
* Menus:
定义该权限组可以访问哪些菜单，若该权限组可以访问某父菜单，父菜单对应的子菜单会显示出来
若不想显示其子菜单，可以把其子菜单加入 "Useablity/No One" 权限组。
* Access Right:
定义该权限组可以**访问哪些对象**，以及拥有 增、查、改、删的哪个权限  (create,read,write,unlink)
* Record Rule:
定义该权限组可以访问**对象中的哪些记录**，以及拥有 增、查、改、删的哪个权限，Access Right是对对象中的**所有记录**赋权限，Record Rule 则通过定义 **domain** 过滤指定**某些记录**赋权限 ['&',('department','=',user.context_department_id.id),('state','=','pr_draft')] 申购单的部门等于当前用户的部门，且申购单的状态是草稿状态
        
### 基于组的访问控制
* 视图中
运用group_id

```xml
<record id="view_order_form_editable_list" model="ir.ui.view">
    <field name="name">sale.order.form.editable.list</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form" />
    <field name="group_id" eval="[(6,0,[ref('product.group.uos'),
         ref('product.group_stock_packaging'),
         ref('sale.group_mrp_properties')])]" />
    <field name="arch" type="xml">
        <xpath expr="//field[@name='order_line]/tree" position="before"
            <attribute name="editable" />
        </xpath>    
    </field>
</record>

* eval: 把eval的值通过作为python运算返回该属性
* ref: 视图的方法，根据 module_name.xml_id 返回数据库id
[(6,0,[xx,yy])]
(0,_ ,{’field’: value}) 这将创建一个新的记录并连接它
(1,id,{’field’: value}): 这是更新一个已经连接了的记录的值
(2,id,_) 这是删除或取消连接某个已经连接了的记录
(3,id,_) 这是取消连接但不删除一个已经连接了的记录
(4,id,_) 连接一个已经存在的记录
(5,_,_) 取消连接但不删除所有已经连接了的记录
(6,_,[ids]) 用给出的列表替换掉已经连接了的记录
这里的下划线一般是0或False

```xml
<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
    <record model="ir.module.category" id="exercises">
      <field name="name">Exercise</field>
    </record>
    <record id="exercise1_submit" model="res.groups">
        <field name="name">submit</field>
        <field name="category_id" ref="exercises"/>
    </record>
    <record id="exercise1_decide" model="res.groups">
        <field name="name">exercise1_decide</field>
        <field name="category_id" ref="exercises"/>
    </record>
</data>
</openerp>

### 访问权限管理：
对于其内的数据访问权限管理有两种机制: 
1. 是模型访问权限管理 (access right)；
2. 是记录规则管理 (record rule)。
record rule 是对access right的细化 ，带条件，比如记录是什么状态的可以访问
如果不为模块设置规则，默认只有Administator才能访问这个模型的数据
record rule 对 Administator 用户是无效的，而 access right 还是有效
   
* access right
权限对象模型是 **ir.model.access.csv**；现在更多的用**ir.model.access.xml**
一般是放在security 文件夹下的 ir.model.access.csv 文件来管理的
文件表头如下：
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

来一个例子：
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_account_payment_term,account.payment.term,model_account_payment_term,account.group_account_user,1,0,0,0

分析这个是针对 account.payment.term 这个模型做访问权限设置
可以看一下对应模型定义的代码：

```python
class account_payment_term(osv.osv):
  _name = "account.payment.term"
  _description = "Payment Term"

* id: 权限的ID不可重复 一般取名为 access_模型名（用下划线连起来）
* name 描述 一般命名沿用模型名用“.”连接
* model_id:id：对象，命名是model_模型名（用下划线连起来）
* group_id:id  组名称 （模块.用户组名）

下面的，0 表示无权限， 1 表示有权限
* perm_read  只读
* perm_write 修改
* perm_create 创建
* perm_unlink 删除


xml例子：

```xml
<?xml version='1.0' encoding='utf-8'?>
<openerp>
    <data>
        <record model="ir.model.access" id="exercise_user_submit">
            <field name="name">申请者</field>
            <field name="model_id" ref="exercise1.model_exercise_two"/>
            <field name="group_id" ref="exercise1.exercise1_submit"/>
            <field eval="True" name="perm_read"/>
            <field eval="True" name="perm_write"/>
            <field eval="True" name="perm_create"/>
            <field eval="False" name="perm_unlink"/>
        </record>
        <record model="ir.model.access" id="exercise_user_submit">
            <field name="name">申请者</field>
            <field name="model_id" ref="exercise1.model_exercise_one"/>
            <field name="group_id" ref="exercise1.exercise1_submit"/>
            <field eval="True" name="perm_read"/>
            <field eval="True" name="perm_write"/>
            <field eval="True" name="perm_create"/>
            <field eval="False" name="perm_unlink"/>
        </record>
        <record model="ir.model.access" id="exercise_user_decide">
            <field name="name">决定者</field>
            <field name="model_id" ref="exercise1.model_exercise_one"/>
            <field name="group_id" ref="exercise1.exercise1_decide"/>
            <field eval="True" name="perm_read"/>
            <field eval="True" name="perm_write"/>
            <field eval="True" name="perm_create"/>
            <field eval="False" name="perm_unlink"/>
        </record>
    </data>
</openerp>

   
### record rule     
一般是放在 security 文件夹下的 **模块名_record_rules.xml** 文件来管理的； 写在 modulename_security.xml 中

```xml
<?xml version='1.0' encoding='utf-8'?>
<openerp>
  <data noupdate=”1”>
      <record id=”todo_task_user_rule” model=”ir.rule”>
          <field name=”name”>ToDo Tasks only for owner</field>
          <field name=”model_id” ref=”model_todo_task”/>
          <field name=”domain_force”>[(’create_uid’,’=’,user.id)]</field>
          <field name=”groups” eval=”[(4,ref(’base.group_user’))]”/>
          <field name="perm_read" eval="1" />
          <field name="perm_write" eval="1" />
          <field name="perm_create" eval="1" />
          <field name="perm_unlink" eval="1" />
      </record>
  </data>
</openerp>   

* record rule: 记录是 ir.rule 模型， 存在public.ir_rule 表格中
* model_id 作用于哪个模型
* domain_force 对该模型中所有记录进行某种过滤操作
* noupdate 值为1 表示升级模块不会更新本数据
* base.group_user 是人力资源 / 雇员
    
    
### 来一个完整的例子解说：

1. 建立组, A_security.xml

```xml
<record id="group_department_project_admin" model="res.groups">
  <field name="name">A</field>
  <field name="category_id" ref="B"/>
  <field name="users" eval="[(4, ref('base.user_root'))]"/> <!-- 把admin用户加入该组中 -->
</record>

* name 组名称
* category_id 属于哪个应用程序，或者哪个模块，为了方便管理
* users 组里面的用户
这样B应用程序就建立了一个名叫A的组。并且初始化了A组的一个用户admin
    
2. 组控制菜单显示 A_view.xml

```xml
<record model="ir.ui.menu" id=" memu_id1">
  <field name="name" >menu1</field>
  <field name="groups_id" eval="[(6,0,[ref('A'),ref('B')]),]"/>           
  <field name="sequence">1</field>
</record>

* name 菜单名称
* groups_id 哪些组可以访问该菜单
* sequence 该菜单的序号
这样A组与B组的成员都可以访问menu1菜单，menu1菜单的显示顺序为1 
注：eval 后面解释，多个组访问用“，”隔开    

<menuitem id="menu_id2 " name="menu2" parent="menu_id1" sequence="1" groups="A,B "/>
* name 菜单名称
* parent 父类菜单 如果没有可以不写parent
* groups哪些组可以访问该菜单
这样menu1的子菜单menu2可以被A组合B组的成员访问
    
3. 权限规则 A_record_rule.xml

```xml
<record model="ir.rule" id="rule1">
  <field name="name">rule1</field>
  <field name="model_id" ref="model_model1"/>
  <field name="global" eval="True"/>
  <field name="domain_force">[1,’=’,1]</field>
  <field name="groups" eval="[(4,ref('A'))]"/>
</record>

* name 规则名称
* model_id 依赖的模块
* global 是否是全局
* domain_force 过滤条件
* groups 属于哪个组

这样A组的成员就可以取到model_model1的所有数据
    
4. ir.model.access.csv
* id 随便取
* name 随便取
* model_id:id 这个就是你所定义的对象了
* group_id:哪个组
* "perm_read","perm_write","perm_create","perm_unlink" 增删改查权限了。1代表有权限
    
    
### Eval
many2many
(0,0,{values}) 根据values里面的信息新建一个记录。
(1,ID,{values})更新id=ID的记录（写入values里面的数据）
(2,ID) 删除id=ID的数据（调用unlink方法，删除数据以及整个主从数据链接关系）
(3,ID) 切断主从数据的链接关系但是不删除这个数据
(4,ID) 为id=ID的数据添加主从链接关系。
(5) 删除所有的从数据的链接关系就是向所有的从数据调用(3,ID)
(6,0,[IDs]) 用IDs里面的记录替换原来的记录（就是先执行(5)再执行循环IDs执行（4,ID））

例子[(6, 0, [8, 5, 6, 4])] 设置 many2many to ids [8, 5, 6, 4]
one2many
(0, 0,{ values })根据values里面的信息新建一个记录。
(1,ID,{values}) 更新id=ID的记录（对id=ID的执行write 写入values里面的数据）
(2,ID) 删除id=ID的数据（调用unlink方法，删除数据以及整个主从数据链接关系）
例子：
[(0,0,{'field_name':field_value_record1,...}),(0,0,{'field_name':field_value_record})]
many2one的字段比较简单，直接填入已经存在的数据的id或者填入False删除原来的记录。
    
### 隐藏的常用技巧

* 直接隐藏
 <group name="owner" position="attributes">
        <attribute name="invisible">True</attribute>
 </group>

* 满足某些条件的隐藏

<xpath expr="//field[@name='parent_id']" position='attributes'>
  <attribute name="attrs">{'invisible': [('passenger','=', True)]}</attribute>
</xpath>
<group col="4" string='旅客信息' attrs="{'invisible': [('supplier','=', True)]}"></group>

* 通过组来隐藏

<xpath expr="//field[@name='type']" position="attributes">
  <attribute name="groups">base.group_no_one</attribute>
</xpath>

* 菜单的隐藏

<record model="ir.ui.menu" id="crm.menu_crm_opportunities">
  <field eval="[(6,0, [ref('base.group_no_one'),])]" name="groups_id"/>
</record>
      
* 代码分析中的运用
1. 字段显示权限

<field name="company_id" groups="base.group_multi_company" widget="selection"/>
  
2.在model中判断

self.pool.get('res.users').has_group(cr, uid, 'sale.group_discount_per_so_line')  

