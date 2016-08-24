---
layout: post
title: "[MOOC]分析linux system_call中断处理过程"
description: "system_call中断处理过程"
category: linux
tags: [linux, kernel]
---

 -  周立维 原创作品转载请注明出处
 - 《Linux内核分析》MOOC课程http://mooc.study.163.com/course/USTC-1000029000

##  系统调用 getpid

选用的系统调用为`getpid`，调用号为20 (/linux-3.18.6/arch/x86/syscalls/syscall_32.tbl)：

    20	i386	getpid			sys_getpid

## 添加 MenuOS 菜单

在 menu/test.c 中添加如下两个函数： GetPid()是直接调用库函数， 而GetPidAsm()是用汇编方式实现。

{% codeblock lang:c %}
int GetPid(int argc, char *argv[])
{
    pid_t pid = getpid();
    printf("pid: %d\n", pid);
    return 0;
}

int GetPidAsm(int argc, char *argv[])
{
    pid_t pid;
    asm volatile(
        "mov $0x14, %%eax\n\t"
        "int $0x80\n\t"
        "mov %%eax, %0\n\t"
        : "=m"(pid)
    );
    printf("pid-asm: %d\n", pid);
    return 0;
}
{% endcodeblock %}

同时在main()中添加新的菜单项。

{% codeblock lang:c %}
int main() 
{
...
    MenuConfig("pid", "Show Current PID", GetPid);
    MenuConfig("pid-asm", "Show Current PID(asm)", GetPidAsm);
    ExecuteMenu();
}
{% endcodeblock %}

再 gcc 编译， 生成新的 rootfs.img， 启动 qemu。
如下是运行截图：

![MenuOS][1]

## system_call 流程分析

在*test.c*中定义的`GetPidAsm`直接使用汇编指令`int $0x80`来进行系统调用： 先将`getpid`的系统调用号0x14放入`%eax`, `int $0x80`指令之后将返回值从`%eax` 放回 `pid`， 最后打印出来。

`int $0x80` 触发软件中断， 代码进入到中断处理函数 `system_call` 中， 即为系统调用处理函数。 `system_call` 的对应的中断在如下文件中设置：

<pre>
/linux-3.18.6/init/main.c
asmlinkage __visible void __init start_kernel(void)
561	trap_init();

/linux-3.18.6/arch/x86/kernel/traps.c
void __init trap_init(void)
838 #ifdef CONFIG_X86_32
839	 set_system_trap_gate(SYSCALL_VECTOR, &system_call);
840	 set_bit(SYSCALL_VECTOR, used_vectors);
841 #endif

/linux-3.18.6/arch/x86/include/asm/irq_vectors.h
50 #ifdef CONFIG_X86_32
51 # define SYSCALL_VECTOR			0x80
52 #endif
</pre>

再来看看 `system_call` 的定义， 中间删除了两段由宏 `#ifdef CONFIG_X86_ESPFIX32` 包围的代码：

<pre>
/linux-3.18.6/arch/x86/kernel/entry_32.S
489	# system call handler stub
490 ENTRY(system_call)
491	RING0_INT_FRAME			# can't unwind into user space anyway
492	ASM_CLAC
493	pushl_cfi %eax			# save orig_eax
494	SAVE_ALL
495	GET_THREAD_INFO(%ebp)
496					# system call tracing in operation / emulation
497	testl $_TIF_WORK_SYSCALL_ENTRY,TI_flags(%ebp)
498	jnz syscall_trace_entry
499	cmpl $(NR_syscalls), %eax
500	jae syscall_badsys
501 syscall_call:
502	call *sys_call_table(,%eax,4)
503 syscall_after_call:
504	movl %eax,PT_EAX(%esp)		# store the return value
505 syscall_exit:
506	LOCKDEP_SYS_EXIT
507	DISABLE_INTERRUPTS(CLBR_ANY)	# make sure we don't miss an interrupt
508					# setting need_resched or sigpending
509					# between sampling and the iret
510	TRACE_IRQS_OFF
511	movl TI_flags(%ebp), %ecx
512	testl $_TIF_ALLWORK_MASK, %ecx	# current->work
513	jne syscall_exit_work
514
515 restore_all:
516	TRACE_IRQS_IRET
517 restore_all_notrace:
...
530 restore_nocheck:
531	RESTORE_REGS 4			# skip orig_eax/error_code
532 irq_return:
533	INTERRUPT_RETURN
534 .section .fixup,"ax"
535 ENTRY(iret_exc)
536	pushl $0			# no error code
537	pushl $do_iret_error
538	jmp error_code
539 .previous
540	_ASM_EXTABLE(irq_return,iret_exc)
541
...
587	CFI_ENDPROC
588 ENDPROC(system_call)


/linux-3.18.6/arch/x86/include/asm/irqflags.h
145 #define INTERRUPT_RETURN		iret
</pre>

* 493-494 先将 `%eax` 和其它寄存器入栈 (SAVE_ALL), 495-498 根据是根据当前线程状态来决定是否调用 `syscall_trace_entry` 吧？ （不确定根据哪些状态位）
* 499-500 如果系统调用号大于最大调用号 `NR_syscalls`， 则转入 `syscall_badsys`， 设置异常返回值于 `%eax`中
* 501-502 调用对应的系统调用函数。 `sys_call_table` 是起始地址， 由`%eax`中的调用号来确定调用函数的偏移量
* 503~    之后就开始准备返回了，512-513 会对中断信号进行处理
* 530-531 `RESTORE_REGS 4` 从栈中恢复寄存器的值
* 532-533 宏 `INTERRUPT_RETURN` 定义了返回指令 `iret

## 总结

系统调用的大致过程如下：

* 中断 `int $0x80` 触发系统调用， `%eax` 传递系统调用过
* 中断处理函数 `system_call` 先将寄存器的值入栈，先检查中断号， 再调用由 `sys_` 开始的系统函数， 最后从栈恢复寄存器， `iret` 指令返回
* 系统调用结果由 `%eax` 传回

## 参考

* [实验楼代码 linux-3.18.6][2]
* [Linux系统调用过程][3]

  [1]: /images/post/2015-04-05/menuos-system_call.png
  [2]: http://codelab.shiyanlou.com/xref/linux-3.18.6/arch/x86/kernel/entry_32.S
  [3]: http://www.cnblogs.com/lknlfy/archive/2012/07/14/2591366.html

