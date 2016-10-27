# Linux内核之进程管理和调度

管理和调度的任务在于：

1、决定各个进程运行多长时间？何时切换到下一个时间？如何决策下一个进程是哪一个？

2、内核从进程A切换到进程B，再切回进程A时，进程A的执行环境与上一次完全相同


task_struct
内核中使用task_struct的数据结构表示一个进程（include/sched.h)

这个结构体包含了所有特定于其他进程的信息以及关联到整个系统的信息，重要的成员包括：

state ：指定了进程的当前状态(就绪、可中断休眠、不可中断休眠、停止）

rlim数组：Linux提供资源限制，通过setrlimit和getrlimits系统函数进行管理修改。 可以通过proc文件系统查看 /proc/self/limits 

struct nsproxy *nsproxy：指向一组子命名空间（意味着此进程属于该命名空间）

struct task_struct *group_leader：CLONE_THREAD建立的线程组，线程组中主进程称为组长，其他线程通过group_leader指向组长

pid_t pgrp：进程组组长的PID。使用系统调用setpgrp可以合并独立进程到进程组（进程组简化了向组所有成员发送信号的操作）  set_task_pgrp

session：几个进程组可以合并成一个会话。set_task_session

pid_t pid：全局PID

pid_t tgid：全局TGID

struct pid_link pids[PIDTYPE_MAX]：所有共享同一个ID的实例都按进程存储在一个散列表中。（线程组）

struct completion *vfork_done; 支持vfork的完成机制
struct user_struct user; 当前进程的用户 //后来移到 const struct cred *real_cred;
/* objective and real subjective task * credentials (COW) */

union thread_union{

​	struct thread_info thread_info;

​	unsigned long stack[THREAD_SIZE/sizeof(long)] 

} ;   

线程信息和核心态栈共用一个联合体，大部分体系结构使用1-2个内存页来保存thread_union，因此有内存地址对齐的要求。 

//调度相关：

unsigned int policy; 
int prio, static_prio, normal_prio;
unsigned int rt_priority;
const struct sched_class *sched_class;
struct sched_entity se;
struct sched_rt_entity rt;
struct list_head run_list;
cpumask_t cpus_allowed;
unsigned int timeslice;

//文件系统相关：

struct fs_struct *fs;                 文件系统信息

struct files_struct *files        文件描述符信息

struct mm_struct *mm, *active_mm;  虚拟地址空间
命名空间
命名空间创建：fork/clone/unshare

命名空间类型：

struct uts_namespace *uts_ns;  

struct ipc_namespace *ipc_ns;  

struct mnt_namespace *mnt_ns;  

struct pid_namespace *pid_ns;  


PID命名空间
简称PID，用fork/clone产生的每个进程都由进程自动地分配一个新的唯一的PID值。PID命名空间是有层次的组织。子命名空间中的PID对于父命名空间可见，但子命名空间无法看到父命名空间的PID。意味着某个进程具有多个PID，凡是可以看到该进程的命名空间，都会为其分配一个PID。


管理PID
目的在于通过PID能够得到task_struct，或者通过task_struct能够得到PID（具体到某个命名空间的PID)

涉及到的数据结构包括：struct pid_namespace,  struct upid, struct pid,

涉及到一个全局散列表pid_hash


由PID得到struct task_struct：  

1 在pid_hash中查找散列溢出链表， 这个链表的所有节点代表一个struct upid实例。所有这些upid中的ur（即命名空间中的PID)都是相同的。

2 由struct upid通过container_of得到struct pid，由于有可能多个task_struct可能对于一个pid，pid->tasks是这些task_struct链表的头

3 现在我们得到是一个task_struct链表，需要通过task_struct的nsprox比对命名空间，从而确定到底是哪个。

由struct task_struct得到PID：

1 通过task_struct的pid元素得到pid

2 由pid和命名空间得到upid

3 upid得到PID


内核中封装了一些调用函数：pid_nr_ns, pid_nr, pid_vnr， task_pid_nr_ns, task_tgid_nr_ns, find_task_by_pid_ns, find_task_by_vpid,find_task_by_pid等

生成PID

alloc_pidmap


进程管理
fork/vfork/clone
fork建立了父进程的一个完整副本，然后作为子进程执行

vfork不创建父进程的副本，父子进程共享数据

clone产生线程，可以对父子进程之间的共享、复制进程精确控制。通过寄存器参数传递标志，不再复制父进程的栈而是可以指定新的栈地址（可能出现线程与父进程共享地址空间，但线程自身的栈可能在另一个地址空间）。

写时复制（COW）

复制进程时只是复制其页表，同时对父子进程的页表的页进行只读标记。若两个今晨只能读取页内存，那么数据共享不是问题。若其中一个进程试图向复制的内存页写入数据会触发缺页异常，内核会检查是否是COW页，进而创建该页专用于当前进程的副本。

copy_process

fork/vfork/clone最终调用了do_fork，这个函数的主要工作在copy_process。该函数的主要工作包括：dup_task_struct/sched_fork/copy_xxx

dup_task_struct

名字就代表了它的功能，为新的内存/进程申请了内存，并且拷贝了父进程的task_struct副本。 需要注意的是，父子进程的所有数据都相同除了栈信息。task_struct->stack。

sched_task

使用调度器对新进程进行设置，主要初始化一些统计字段，并且在各个CPU之间对可用进程重新均衡。

这需要禁止抢占，然后设置优先级值和调度类，以及作为调度实体中提供给调度类的一些信息。

copy_xxx

若是传入了标志CLONE_XXX，则说明可以和父进程共享XXX的资源，不过需要将XXX的引用技术增加1

pid关系

使用pid_nr得到全局PID，设置pid和tgid。对于tgid，若生成是线程，则需要设置成父进程的tgid。

parent/child关系


if (clone_flags & (CLONE_PARENT|CLONE_THREAD)) {  

​	p->real_parent = current->real_parent;  
​	p->parent_exec_id = current->parent_exec_id;  
} else {  
​	p->real_parent = current;  
​	p->parent_exec_id = current->self_exec_id;  
}  

组关系
组成父子关系、线程组、会话组信息。

kernel_thread/kthread_create/kthread_run/kthread_create_cpu
内核线程由内核本身启动的进程。大多数计算机上系统的全部虚拟地址空间分为两个部分：用户层程序访问、内核使用。内核代表用户程序运行时，虚拟地址空间的用户空间部分由mm描述。每当内核执行上下文切换时，虚拟地址空间的用户层部分都会切换，以便与当前运行的进程匹配。

内核线程的mm为空，且进程被称为惰性TLB进程。

启动新程序：execve系统调用
这需要通过新代码替换现存程序，Linux提供了execve系统调用，这个函数的主要工作由do_execve完成。需要打开要执行的文件，分析文件格式，使用对应的处理类处理程序执行。 最关键的时将应用程序映射到虚拟地址空间中。


退出进程：exit系统调用
进程使用exit系统调用终止，它会将各个引用计数减1，如果引用计数器归0而没有进程再使用对应的结构，那么相应的内存区域返回给内存管理模块。


进程调度
目的在于让各个进程尽可能地公平共享CPU时间，同时考虑不同的任务优先级。

内核中存在两个调度器：主调度器/周期性调度器。 这两个调度器称为通用调度器或核心调度器。 调度器使用调度类判断接下来运行哪个进程，在选中将要运行的进程后必须执行底层任务切换

调度相关数据结构
task_struct

这个结构体中表示优先级的有3个元素：static_prio,normal_prio, prio。分别表示静态（启动时分配）、普通（静态优先级+调度策略）、动态优先级（可临时提高）。


struct sched_class
这个结构体提供了通用调度器（核心调度器）和各个调度方法之间的关联。这个结构体包括的操作：

enqueue_task/dequeue_task，操作就绪队列

sched_yield进程放弃对处理器的控制权

check_preemp_cur 用一个新进程来抢占当前进程

pick_next_task选择下一个将要运行的进程

set_curr_task 调度测率发生变化时

task_tick 每次激活周期性调度器时

new_task 用于fork系统调用和调度器之间的联系。


struct rq

内核提供了struct rq数据结构用于表示就绪队列，并为系统所有就绪队列声明了runqueues数组中，该数组每个元素对应一个CPU
static DEFINE_PER_CPU_SHARED_ALIGNED(struct rq,runqueues)  
就绪队列是全局调度器许多操作的起点，就绪队列中的进程由各个调度器类直接管理（出入队列、查询等）

struct sched_entity

调度器可以操作比进程更一般的实体，这个结构体中比较重要的元素包括：

load: 调度实体的权重，它与就绪队列中的负荷比作为调度算法的重要参考依据

run_node: 有了它就可以将调度实体放入红黑树

on_rq：是否接受调度

sum_exec_runtime/prev_sum_exec_runtime：记录消耗的CPU时间（注意是物理时间）

vruntim：记录消耗的虚拟时间


调度实体的优先级
如何计算优先级

一般情况下，调度器考虑的有效级是prio(动态优先级），计算方法：effective_prio(); 

计算负荷权重

进程的重要性不仅由优先级指定，而且需要考虑保存在task_struct->se.load的负荷权重。

set_load_weight负责根据进程类型及其静态优先级计算负荷权重。

实时进程的进程的权重是普通进程的两倍（实际上时普通进程最大权重的2倍）

idle进程则使用默认的权重

当进程添加到就绪队列时，内核会调用inc_nr_running，修改就绪队列中的进程数并且累加进程的负荷值。


实际应用中，普通进程的优先级、负荷权重在判断是否抢占时有用，负荷权重在计算应得的运行时间有用。


核心调度器（通用调度器）
调度器的实现基于两个函数：周期性调度器函数和主调度器函数：
scheduler_tick（周期性调度器函数）
1、管理内核中与整个系统和各个进程的调度相关的统计量
2、激活负责当前进程的调度类的周期性调度方法。（rq->curr->sched_class->task_tick）

schedule（主调度器函数）
将CPU分配给与当前活动进程不同的另一个进程
1、先设置TIF_NEED_RESCHED标志,
2、若当前为可中断进程且有信号未处理时，需要将当前进程重新设置位可就绪的，否则dequeue当前进程，并调用put_prev_task和pick_next_task。
3、进程的切换需要调用context_switch执行底层上下文切换（如下）。
context_switch称为上下文切换，主要工作由两个函数完成：switch_mm和switch_to

* switch_mm

  使用task_struct->mm的内存管理上下文，对底层进行：加载页表、刷出地址转换后被缓冲器（部分或全部）、向内存管理单元（MMU）提供新的信息   

* switch_to

  切换处理器寄存器内容和内核栈       


switch_to
switch_to完成了上下文切换的关键点，之后的代码只有当进程再次被切换回来的时候才能调用。 例如进程A切换到B，再从B到C，最后回到A。
按时间点执行过程如下：
1、进程A切换到B，switch_to之前的prev是A，next是B。且prev和next都在栈空间里。
2、执行B进程
3、..其他进程...
4、其他进程切换回A，此时需要恢复A的上下文，这样进程A看到的所有数据和在第1步时看到的数据信息应该是一样的。 那么问题来了，这时候会发现prev还是A。显然这是不对的。
看看mips的实现
[cpp] view plain copy

\#define switch_to(prev, next, last)    \

do {                                    \  

​	__mips_mt_fpaff_switch_to(prev);                \  

​	if (cpu_has_dsp)                        \  

​		__save_dsp(prev);                   \  

​	__clear_software_ll_bit();                  \  

​	(last) = resume(prev, next, task_thread_info(next));        \  

} while (0)  

\_\_mips_mt_fpaff_switch_to和 \_\_save_dsp与具体mips硬件结构相关，先忽略掉。
\_\_clear_software_ll_bit用于处理ll指令和sc指令，也忽略掉
r4k 的resume的实现如下

```c
/* 
 * task_struct *resume(task_struct *prev, task_struct *next, 
 *                     struct thread_info *next_ti) 
 */  
    .align  5  
    LEAF(resume)  
    mfc0    t1, CP0_STATUS  
    LONG_S  t1, THREAD_STATUS(a0)  //存放CP0_STATUS  
    cpu_save_nonscratch a0         //存s0-s7 sp fp  
    LONG_S  ra, THREAD_REG31(a0)   //存ra  
  
    /* 
     * check if we need to save FPU registers 
     */  
    PTR_L   t3, TASK_THREAD_INFO(a0)  //处理FPU寄存器  
    LONG_L  t0, TI_FLAGS(t3)  
    li  t1, _TIF_USEDFPU  
    and t2, t0, t1  
    beqz    t2, 1f                   //不需要保存FPU  
    nor t1, zero, t1  
  
    and t0, t0, t1  
    LONG_S  t0, TI_FLAGS(t3)  
  
    /* 
     * clear saved user stack CU1 bit 
     */  
    LONG_L  t0, ST_OFF(t3)  
    li  t1, ~ST0_CU1  
    and t0, t0, t1  
    LONG_S  t0, ST_OFF(t3)  
  
    fpu_save_double a0 t0 t1        # c0_status passed in t0  
                        # clobbers t1  
1:  
  
    /* 
     * The order of restoring the registers takes care of the race 
     * updating $28, $29 and kernelsp without disabling ints. 
     */  
    move    $28, a2                           //<span style="color:#ff0000;">gp存储next_ti指针的值</span>  
    cpu_restore_nonscratch a1                 //恢复next的s0-s7 sp fp ra寄存器数据  
  
    PTR_ADDU    t0, $28, _THREAD_SIZE - 32 //获取恢复调度之前上个活动进程设置的next_ti  
    set_saved_sp    t0, t1, t2  
#ifdef CONFIG_MIPS_MT_SMTC  
    /* Read-modify-writes of Status must be atomic on a VPE */  
    mfc0    t2, CP0_TCSTATUS  
    ori t1, t2, TCSTATUS_IXMT  
    mtc0    t1, CP0_TCSTATUS  
    andi    t2, t2, TCSTATUS_IXMT  
    _ehb  
    DMT 8               # dmt   t0  
    move    t1,ra  
    jal mips_ihb  
    move    ra,t1  
#endif /* CONFIG_MIPS_MT_SMTC */  
    mfc0    t1, CP0_STATUS      //修改CP0_STATUS  
    li  a3, 0xff01  
    and t1, a3  
    LONG_L  a2, THREAD_STATUS(a1)  
    nor a3, $0, a3  
    and a2, a3  
    or  a2, t1  
    mtc0    a2, CP0_STATUS  
#ifdef CONFIG_MIPS_MT_SMTC  
    _ehb  
    andi    t0, t0, VPECONTROL_TE  
    beqz    t0, 1f  
    emt  
1:  
    mfc0    t1, CP0_TCSTATUS  
    xori    t1, t1, TCSTATUS_IXMT  
    or  t1, t1, t2  
    mtc0    t1, CP0_TCSTATUS  
    _ehb  
#endif /* CONFIG_MIPS_MT_SMTC */  
    move    v0, a0                             //返回指针指向a0，即当前调度之前的活动进程  
    jr  ra                                 //跳转到next保存的ra寄存器指向的地址  
    END(resume)  
```

上述代码代码主要实现了寄存器的保存和恢复（task_struct->thread_info)。需要注意的是，保存和恢复的寄存器只局限于S0-S7 ,Sp,FP,RA,CP0等。对于像A->B这样的调度，resume返回值就是A的指针值，利用的是a0-a3参数寄存器不保存的特性。


和fork的交互
fork系统调用会用到sched_fork，将调度器类挂钩到该进程。
fork的后期会调用wake_up_new_task唤醒新的进程，这时，会将新进程加入到相应调度器类的就绪队列中。



完全公平调度类
数据结构
struct sched_fair_sched_class声明操作函数
struct cfs_rq定义CFS就绪队列：
struct load_weight load;              负载
unsignd long nr_running;            当前队列中的进程个数
u64 min_vruntime                       最小虚拟运行时间
struct rb_root tasks_timeline      红黑树根
struct rb_node* rb_leftmost;      红黑树最左边
struct sched_entry* curr;           当前调度实体

调度算法
CFS没有使用时间片的概念，它对每个进程累计各自的虚拟运行时间sched_entity->vruntime, 同时更新cpu的运行时间cfs_rq->min_vruntime。
为了完全公平，每个进程的vruntime都应该差不多，且和实际的CPU的min_vruntime差不多。 不过CPU一直在运行，有些进程却可能停止、休眠，因此一般来说进程的vruntime比CPU的min_vruntime要小一些，vruntime一直在追赶min_vruntime。

内核将这些进程以(vruntime-min_vruntime)为键值，构造了一棵红黑树，越左边的值越小。

update_curr函数更新vruntime/min_vruntime
当前运行进程的vruntime在update_curr函数中进行更新。 每次增加的虚拟时间=物理时间*NICE_0_LOAD/curr->load.weight。 增加的虚拟时间和当前调度实体的权重成反比，因此权重越大，每次增加的虚拟时间就愈少。（而优先级或调度策略越高则权重越大）从而优先级高的进程在红黑树向右移动的速度越慢。

对于min_vruntime，总是希望它是单调递增的，所以在最后更新时取的时所有vruntime的max值。


延迟跟踪
内核保证每个可运行的进程都应该至少运行一次的某个时间间隔（注意不是至少运行一段时间）：
sysctl_sched_latency*nr_running/sched_nr_latency
其中：
sysctl_sched_latency(/proc/sys/kernel/sched_latency_ns，默认20000000纳秒20毫秒)控制默认的调度延迟
sched_nr_latency 控制延迟周期中处理的最大活动进程数目。计算方式：sysctl_sched_latency/sysctl_sched_min_granularity
在这个延迟周期内，活动进程分配到的时间和进程的权重成正比（sched_slice)。


enqueue_task_fair
将进程添加到就绪队列中，实际上就是加入到红黑树上。如果进程之前睡眠的话需要使用place_entity调整进程的虚拟时间。 其中涉及到的技巧：
若是旧的休眠进程，需要保证在当前延迟周期结束后才能运行，直接将进程vruntime减去sysctl_sched_latency。
若是新建的进程，为了使得新进程比父进程先运行，会增加一些值(sched_vslice_add)

pick_next_task_fair
选择最左边的节点，并赋值给cfs_rq->curr。

check_preempt_tick处理周期性调度器 / check_preempt_wakeup 唤醒抢占
周期性调度器会调用完全公平调度器类定义的task_tick_fair函数，其主要工作由entity_tick完成。红黑树上进程树不能小于2个。使用check_preempt_tick查找新的进程。这个函数的目的在于：确保当前进程不会比延迟周期中确定的份额运行得更长，否则会调用resched_task(rq_of(cfs_rq)->curr)发出重新调度请求。（在task_struct中设置TIF_NEED_RESCHED标志，核心调度器会在下一个合适时机发起新调度）

内核在try_to_wake_up和wake_up_new_tassk时会调用check_preempt_curr函数查看是否新进程可以抢占当前的进程。
新唤醒的进程不必一定由完全公平调度器处理（实时进程触发重新调度）
内核确保被抢占者运行了某一个最小时间间隔（sysctl_sched_wakeup_granularity，避免太过频繁调度）
最终的结果会导致resched_task(curr)，从而设置curr的TIF_NEED_RESCHED标志位。

task_new_fair新进程处理
可以使用sysctl_sched_child_runs_first控制新进程优先父进程运行

实时调度类
主要涉及了一些新的数据结构：struct rt_sched_class、struct rq、struct rt_prio_array
使用了时间片的概念
