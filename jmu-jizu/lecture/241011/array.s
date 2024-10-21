	.file	"array.c"
	.text
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	endbr64
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movq	%fs:40, %rax
	movq	%rax, 24(%rsp)
	xorl	%eax, %eax
	movw	$10, 4(%rsp)
	movw	$15, 6(%rsp)
	movw	$20, 8(%rsp)
	movw	$25, 10(%rsp)
	movw	$30, 12(%rsp)
	movl	$1, %ecx
	jmp	.L2
.L3:
	movslq	%ecx, %rsi
	movzwl	4(%rsp,%rsi,2), %edx
	movswl	%dx, %eax
	imull	$26215, %eax, %eax
	sarl	$17, %eax
	sarw	$15, %dx
	subl	%edx, %eax
	leal	(%rax,%rax,2), %eax
	movw	%ax, 14(%rsp,%rsi,2)
	addl	$1, %ecx
.L2:
	cmpl	$4, %ecx
	jle	.L3
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L6
	addq	$40, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L6:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
