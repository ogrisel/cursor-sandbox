	.file	"<string>"
	.section	.ltext,"axl",@progbits
	.globl	_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$264, %rsp
	.cfi_def_cfa_offset 320
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rdx, %r15
	movq	%rsi, %r14
	movq	%rdi, %r13
	movq	360(%rsp), %r12
	movq	336(%rsp), %rbp
	movabsq	$NRT_incref, %rbx
	movq	%rdx, %rdi
	callq	*%rbx
	movq	%r12, %rdi
	callq	*%rbx
	testq	%rbp, %rbp
	js	.LBB0_62
	movq	%rbp, %rdx
	imulq	%rbp, %rdx
	movabsq	$.const.picklebuf.139798927689024, %rax
	jo	.LBB0_64
	movabsq	$-1152921504606846976, %rcx
	movabsq	$-2305843009213693952, %rsi
	addq	%rdx, %rcx
	cmpq	%rsi, %rcx
	jb	.LBB0_64
	movq	%rdx, 72(%rsp)
	leaq	(,%rdx,8), %rbx
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	movq	%rbx, %rdi
	movl	$32, %esi
	callq	*%rax
	testq	%rax, %rax
	je	.LBB0_63
	movq	%rax, %rcx
	movq	%r13, 136(%rsp)
	movq	%r15, 144(%rsp)
	movq	%r14, 160(%rsp)
	leaq	(,%rbp,8), %rax
	movq	%rax, (%rsp)
	movq	%rcx, 128(%rsp)
	movq	24(%rcx), %r14
	movabsq	$memset, %rax
	movq	%r14, %rdi
	xorl	%esi, %esi
	movq	%rbx, %rdx
	callq	*%rax
	testq	%rbp, %rbp
	movq	72(%rsp), %rcx
	je	.LBB0_54
	movq	320(%rsp), %rax
	leaq	31(%rbp), %rcx
	shrq	$5, %rcx
	movq	%rcx, 64(%rsp)
	movabsq	$9223372036854775792, %rcx
	movq	%rbp, %rdx
	shlq	$8, %rdx
	movq	%rdx, 80(%rsp)
	leaq	96(%rax), %rdx
	movq	%rdx, 56(%rsp)
	leaq	96(%r14), %rdx
	movq	%rdx, 40(%rsp)
	xorl	%edx, %edx
	addq	$12, %rcx
	movq	%rcx, 168(%rsp)
	movq	%r14, 32(%rsp)
	movq	%rax, 48(%rsp)
	movq	%r14, 120(%rsp)
.LBB0_6:
	movq	%rdx, %rax
	shlq	$5, %rax
	leaq	32(%rax), %r13
	cmpq	%r13, %rbp
	cmovlq	%rbp, %r13
	subq	%rax, %r13
	js	.LBB0_55
	movq	%rdx, %rax
	shlq	$8, %rax
	incq	%rdx
	movq	%rdx, 152(%rsp)
	leaq	(,%r13,8), %rcx
	leaq	(%r14,%rax), %rdx
	movq	%rdx, 192(%rsp)
	leaq	(%rdx,%r13,8), %rdx
	movq	%rdx, 184(%rsp)
	addq	320(%rsp), %rax
	movq	%rax, 224(%rsp)
	leaq	(%rax,%r13,8), %rax
	movq	%rax, 216(%rsp)
	movq	%r13, %r12
	movabsq	$9223372036854775792, %rax
	andq	%rax, %r12
	movq	%r13, %r14
	andq	168(%rsp), %r14
	movq	%rcx, 24(%rsp)
	orq	(%rsp), %rcx
	movq	%rcx, 176(%rsp)
	movq	32(%rsp), %rax
	movq	%rax, 96(%rsp)
	movq	40(%rsp), %rax
	movq	%rax, 88(%rsp)
	xorl	%edx, %edx
	jmp	.LBB0_9
	.p2align	4
.LBB0_8:
	movq	112(%rsp), %rbx
	incq	%rbx
	movq	208(%rsp), %rdi
	movabsq	$NRT_decref, %rax
	vzeroupper
	callq	*%rax
	movq	%rbx, %rdx
	movq	80(%rsp), %rax
	addq	%rax, 88(%rsp)
	addq	%rax, 96(%rsp)
	cmpq	64(%rsp), %rbx
	movq	72(%rsp), %rcx
	je	.LBB0_53
.LBB0_9:
	movq	%rdx, %rax
	shlq	$5, %rax
	leaq	32(%rax), %rsi
	cmpq	%rsi, %rbp
	cmovlq	%rbp, %rsi
	movq	%rax, 248(%rsp)
	subq	%rax, %rsi
	movl	$1, %r15d
	testq	%rsi, %rsi
	cmovleq	%rsi, %r15
	js	.LBB0_55
	movq	%rsi, %rbp
	imulq	%r13, %rbp
	jo	.LBB0_58
	movabsq	$-1152921504606846976, %rax
	addq	%rbp, %rax
	movabsq	$-2305843009213693952, %rcx
	cmpq	%rcx, %rax
	jb	.LBB0_58
	movq	%rsi, 8(%rsp)
	movq	%rdx, 112(%rsp)
	shlq	$3, %rbp
	movq	%rbp, %rdi
	movl	$32, %esi
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	callq	*%rax
	testq	%rax, %rax
	je	.LBB0_56
	movq	8(%rsp), %rcx
	subq	%r15, %rcx
	movq	%rcx, 200(%rsp)
	leaq	8(,%rcx,8), %rcx
	imulq	%r13, %rcx
	movq	%rcx, 104(%rsp)
	movq	%rax, 208(%rsp)
	movq	24(%rax), %rdi
	movq	%rdi, 16(%rsp)
	xorl	%esi, %esi
	movq	%rbp, %rdx
	movabsq	$memset, %rax
	callq	*%rax
	cmpq	$0, 328(%rsp)
	movq	336(%rsp), %rbp
	movq	(%rsp), %r11
	jle	.LBB0_36
	cmpq	$0, 8(%rsp)
	movq	16(%rsp), %rax
	je	.LBB0_8
	testq	%r13, %r13
	jle	.LBB0_8
	movq	104(%rsp), %rcx
	addq	%rax, %rcx
	movq	%rcx, 240(%rsp)
	addq	$96, %rax
	movq	%rax, 232(%rsp)
	movq	48(%rsp), %rdx
	movq	56(%rsp), %rsi
	xorl	%edi, %edi
	jmp	.LBB0_18
	.p2align	4
.LBB0_17:
	movq	256(%rsp), %rdi
	incq	%rdi
	movq	(%rsp), %r11
	addq	%r11, %rsi
	addq	%r11, %rdx
	cmpq	%rdi, 328(%rsp)
	movq	336(%rsp), %rbp
	je	.LBB0_36
.LBB0_18:
	cmpq	$0, 24(%rsp)
	sets	%al
	movq	%r11, %rcx
	imulq	%rdi, %rcx
	movq	224(%rsp), %r8
	leaq	(%r8,%rcx), %r9
	addq	216(%rsp), %rcx
	movq	392(%rsp), %r8
	vmovsd	(%r8,%rdi,8), %xmm0
	movq	%rdi, 256(%rsp)
	movq	%rdi, %r8
	imulq	%rbp, %r8
	movq	320(%rsp), %r10
	leaq	(%r10,%r8,8), %r8
	movq	248(%rsp), %rdi
	leaq	(%r8,%rdi,8), %r8
	movq	16(%rsp), %r10
	cmpq	%rcx, %r10
	setb	%cl
	cmpq	240(%rsp), %r9
	setb	%r9b
	andb	%cl, %r9b
	orb	%al, %r9b
	movq	232(%rsp), %r11
	movq	8(%rsp), %rax
	xorl	%ebp, %ebp
	jmp	.LBB0_20
	.p2align	4
.LBB0_19:
	leaq	-1(%rax), %rcx
	incq	%rbp
	movq	24(%rsp), %rbx
	addq	%rbx, %r11
	addq	%rbx, %r10
	cmpq	$1, %rax
	movq	%rcx, %rax
	jle	.LBB0_17
.LBB0_20:
	cmpq	$4, %r13
	setb	%cl
	vmulsd	(%r8,%rbp,8), %xmm0, %xmm1
	orb	%r9b, %cl
	testb	$1, %cl
	je	.LBB0_22
	xorl	%ebx, %ebx
	jmp	.LBB0_31
	.p2align	4
.LBB0_22:
	cmpq	$16, %r13
	jae	.LBB0_24
	xorl	%ecx, %ecx
	jmp	.LBB0_28
	.p2align	4
.LBB0_24:
	vbroadcastsd	%xmm1, %ymm2
	xorl	%ecx, %ecx
	.p2align	4
.LBB0_25:
	vmulpd	-96(%rsi,%rcx,8), %ymm2, %ymm3
	vmulpd	-64(%rsi,%rcx,8), %ymm2, %ymm4
	vmulpd	-32(%rsi,%rcx,8), %ymm2, %ymm5
	vmulpd	(%rsi,%rcx,8), %ymm2, %ymm6
	vaddpd	-96(%r11,%rcx,8), %ymm3, %ymm3
	vaddpd	-64(%r11,%rcx,8), %ymm4, %ymm4
	vaddpd	-32(%r11,%rcx,8), %ymm5, %ymm5
	vaddpd	(%r11,%rcx,8), %ymm6, %ymm6
	vmovupd	%ymm3, -96(%r11,%rcx,8)
	vmovupd	%ymm4, -64(%r11,%rcx,8)
	vmovupd	%ymm5, -32(%r11,%rcx,8)
	vmovupd	%ymm6, (%r11,%rcx,8)
	addq	$16, %rcx
	cmpq	%rcx, %r12
	jne	.LBB0_25
	cmpq	%r12, %r13
	je	.LBB0_19
	movq	%r12, %rcx
	movq	%r12, %rbx
	testb	$12, %r13b
	je	.LBB0_31
.LBB0_28:
	vbroadcastsd	%xmm1, %ymm2
	.p2align	4
.LBB0_29:
	vmulpd	(%rdx,%rcx,8), %ymm2, %ymm3
	vaddpd	(%r10,%rcx,8), %ymm3, %ymm3
	vmovupd	%ymm3, (%r10,%rcx,8)
	addq	$4, %rcx
	cmpq	%rcx, %r14
	jne	.LBB0_29
	movq	%r14, %rbx
	cmpq	%r14, %r13
	je	.LBB0_19
.LBB0_31:
	movq	%r12, %rdi
	movl	%r13d, %r15d
	subl	%ebx, %r15d
	movq	%rbx, %rcx
	andl	$7, %r15d
	je	.LBB0_34
	movq	%rbx, %r12
	.p2align	4
.LBB0_33:
	leaq	1(%r12), %rcx
	vmulsd	(%rdx,%r12,8), %xmm1, %xmm2
	vaddsd	(%r10,%r12,8), %xmm2, %xmm2
	vmovsd	%xmm2, (%r10,%r12,8)
	movq	%rcx, %r12
	decq	%r15
	jne	.LBB0_33
.LBB0_34:
	subq	%r13, %rbx
	cmpq	$-8, %rbx
	movq	%rdi, %r12
	ja	.LBB0_19
	.p2align	4
.LBB0_35:
	vmulsd	(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, (%r10,%rcx,8)
	vmulsd	8(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	8(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 8(%r10,%rcx,8)
	vmulsd	16(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	16(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 16(%r10,%rcx,8)
	vmulsd	24(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	24(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 24(%r10,%rcx,8)
	vmulsd	32(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	32(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 32(%r10,%rcx,8)
	vmulsd	40(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	40(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 40(%r10,%rcx,8)
	vmulsd	48(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	48(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 48(%r10,%rcx,8)
	vmulsd	56(%rdx,%rcx,8), %xmm1, %xmm2
	vaddsd	56(%r10,%rcx,8), %xmm2, %xmm2
	vmovsd	%xmm2, 56(%r10,%rcx,8)
	leaq	8(%rcx), %rbx
	movq	%rbx, %rcx
	cmpq	%rbx, %r13
	jne	.LBB0_35
	jmp	.LBB0_19
	.p2align	4
.LBB0_36:
	movq	8(%rsp), %r9
	testq	%r9, %r9
	movq	16(%rsp), %r10
	je	.LBB0_8
	testq	%r13, %r13
	jle	.LBB0_8
	movq	80(%rsp), %rax
	imulq	112(%rsp), %rax
	movq	192(%rsp), %rcx
	addq	%rax, %rcx
	addq	184(%rsp), %rax
	movq	200(%rsp), %rsi
	imulq	%r11, %rsi
	addq	%rax, %rsi
	cmpq	$0, 176(%rsp)
	sets	%dl
	movq	104(%rsp), %rax
	addq	%r10, %rax
	cmpq	%rax, %rcx
	setb	%cl
	cmpq	%rsi, %r10
	setb	%al
	andb	%cl, %al
	orb	%dl, %al
	leaq	96(%r10), %rcx
	movq	96(%rsp), %rdx
	movq	88(%rsp), %rsi
	jmp	.LBB0_40
	.p2align	4
.LBB0_39:
	leaq	-1(%r9), %rdi
	addq	%r11, %rsi
	movq	24(%rsp), %r8
	addq	%r8, %rcx
	addq	%r11, %rdx
	addq	%r8, %r10
	cmpq	$1, %r9
	movq	%rdi, %r9
	jle	.LBB0_8
.LBB0_40:
	cmpq	$4, %r13
	setb	%dil
	orb	%al, %dil
	testb	$1, %dil
	je	.LBB0_42
	xorl	%r8d, %r8d
	jmp	.LBB0_48
	.p2align	4
.LBB0_42:
	xorl	%edi, %edi
	cmpq	$16, %r13
	jb	.LBB0_46
	.p2align	4
.LBB0_43:
	vmovupd	-96(%rsi,%rdi,8), %ymm0
	vmovupd	-64(%rsi,%rdi,8), %ymm1
	vmovupd	-32(%rsi,%rdi,8), %ymm2
	vmovupd	(%rsi,%rdi,8), %ymm3
	vaddpd	-96(%rcx,%rdi,8), %ymm0, %ymm0
	vaddpd	-64(%rcx,%rdi,8), %ymm1, %ymm1
	vaddpd	-32(%rcx,%rdi,8), %ymm2, %ymm2
	vaddpd	(%rcx,%rdi,8), %ymm3, %ymm3
	vmovupd	%ymm0, -96(%rsi,%rdi,8)
	vmovupd	%ymm1, -64(%rsi,%rdi,8)
	vmovupd	%ymm2, -32(%rsi,%rdi,8)
	vmovupd	%ymm3, (%rsi,%rdi,8)
	addq	$16, %rdi
	cmpq	%rdi, %r12
	jne	.LBB0_43
	cmpq	%r12, %r13
	je	.LBB0_39
	movq	%r12, %rdi
	movq	%r12, %r8
	testb	$12, %r13b
	je	.LBB0_48
	.p2align	4
.LBB0_46:
	vmovupd	(%rdx,%rdi,8), %ymm0
	vaddpd	(%r10,%rdi,8), %ymm0, %ymm0
	vmovupd	%ymm0, (%rdx,%rdi,8)
	addq	$4, %rdi
	cmpq	%rdi, %r14
	jne	.LBB0_46
	movq	%r14, %r8
	cmpq	%r14, %r13
	je	.LBB0_39
.LBB0_48:
	movq	%r9, %rbx
	movl	%r13d, %r9d
	subl	%r8d, %r9d
	movq	%r8, %rdi
	andl	$7, %r9d
	movq	%r10, %r15
	je	.LBB0_51
	movq	%r8, %r10
	.p2align	4
.LBB0_50:
	leaq	1(%r10), %rdi
	vmovsd	(%rdx,%r10,8), %xmm0
	vaddsd	(%r15,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%rdx,%r10,8)
	movq	%rdi, %r10
	decq	%r9
	jne	.LBB0_50
.LBB0_51:
	subq	%r13, %r8
	cmpq	$-8, %r8
	movq	%rbx, %r9
	movq	%r15, %r10
	ja	.LBB0_39
	.p2align	4
.LBB0_52:
	vmovsd	(%rdx,%rdi,8), %xmm0
	vmovsd	8(%rdx,%rdi,8), %xmm1
	vaddsd	(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%rdx,%rdi,8)
	vaddsd	8(%r10,%rdi,8), %xmm1, %xmm0
	vmovsd	%xmm0, 8(%rdx,%rdi,8)
	vmovsd	16(%rdx,%rdi,8), %xmm0
	vaddsd	16(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%rdx,%rdi,8)
	vmovsd	24(%rdx,%rdi,8), %xmm0
	vaddsd	24(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%rdx,%rdi,8)
	vmovsd	32(%rdx,%rdi,8), %xmm0
	vaddsd	32(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%rdx,%rdi,8)
	vmovsd	40(%rdx,%rdi,8), %xmm0
	vaddsd	40(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%rdx,%rdi,8)
	vmovsd	48(%rdx,%rdi,8), %xmm0
	vaddsd	48(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%rdx,%rdi,8)
	vmovsd	56(%rdx,%rdi,8), %xmm0
	vaddsd	56(%r10,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%rdx,%rdi,8)
	leaq	8(%rdi), %r8
	movq	%r8, %rdi
	cmpq	%r8, %r13
	jne	.LBB0_52
	jmp	.LBB0_39
	.p2align	4
.LBB0_53:
	addq	$256, 56(%rsp)
	addq	$256, 48(%rsp)
	addq	$256, 40(%rsp)
	addq	$256, 32(%rsp)
	movq	152(%rsp), %rdx
	cmpq	64(%rsp), %rdx
	movq	120(%rsp), %r14
	jne	.LBB0_6
.LBB0_54:
	movq	136(%rsp), %rax
	movq	128(%rsp), %rdx
	movq	%rdx, (%rax)
	movq	$0, 8(%rax)
	movq	%rcx, 16(%rax)
	movq	$8, 24(%rax)
	movq	%r14, 32(%rax)
	movq	%rbp, 40(%rax)
	movq	%rbp, 48(%rax)
	movq	(%rsp), %rcx
	movq	%rcx, 56(%rax)
	movq	$8, 64(%rax)
	movq	360(%rsp), %rdi
	movabsq	$NRT_decref, %rbx
	callq	*%rbx
	movq	144(%rsp), %rdi
	callq	*%rbx
	xorl	%eax, %eax
	jmp	.LBB0_61
.LBB0_55:
	movabsq	$.const.picklebuf.139798927552384, %rcx
	jmp	.LBB0_59
.LBB0_58:
	movabsq	$.const.picklebuf.139798927689024, %rcx
	jmp	.LBB0_59
.LBB0_56:
	movabsq	$.const.picklebuf.139798927748736, %rcx
.LBB0_59:
	movq	160(%rsp), %rax
	movq	%rcx, (%rax)
.LBB0_60:
	movl	$1, %eax
.LBB0_61:
	addq	$264, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.LBB0_62:
	.cfi_def_cfa_offset 320
	movabsq	$.const.picklebuf.139798927552384, %rax
	jmp	.LBB0_64
.LBB0_63:
	movabsq	$.const.picklebuf.139798927748736, %rax
.LBB0_64:
	movq	%rax, (%r14)
	jmp	.LBB0_60
.Lfunc_end0:
	.size	_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end0-_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	_ZN7cpython8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN7cpython8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN7cpython8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$504, %rsp
	.cfi_def_cfa_offset 560
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rsi, %rdi
	movabsq	$".const.main.<locals>.nb_fused_blocked", %rsi
	movabsq	$PyArg_UnpackTuple, %r10
	xorl	%r14d, %r14d
	leaq	200(%rsp), %r8
	leaq	192(%rsp), %r9
	movl	$2, %edx
	movl	$2, %ecx
	xorl	%eax, %eax
	callq	*%r10
	movq	$0, 104(%rsp)
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 208(%rsp)
	vmovups	%ymm0, 240(%rsp)
	movq	$0, 272(%rsp)
	testl	%eax, %eax
	je	.LBB1_23
	movabsq	$_ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
	movq	(%rax), %r12
	testq	%r12, %r12
	je	.LBB1_2
	movq	200(%rsp), %rdi
	vmovups	%ymm0, 368(%rsp)
	vmovups	%ymm0, 400(%rsp)
	movq	$0, 432(%rsp)
	movabsq	$NRT_adapt_ndarray_from_python, %rbx
	leaq	368(%rsp), %rsi
	vzeroupper
	callq	*%rbx
	cmpq	$8, 392(%rsp)
	setne	%cl
	testl	%eax, %eax
	setne	%bpl
	orb	%cl, %bpl
	cmpb	$1, %bpl
	je	.LBB1_5
	testb	%bpl, %bpl
	jne	.LBB1_22
.LBB1_7:
	movq	368(%rsp), %r14
	movq	400(%rsp), %r15
	movq	408(%rsp), %rbp
	movq	416(%rsp), %r13
	movq	192(%rsp), %rdi
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 448(%rsp)
	vmovups	%ymm0, 472(%rsp)
	leaq	448(%rsp), %rsi
	vzeroupper
	callq	*%rbx
	testl	%eax, %eax
	jne	.LBB1_9
	cmpq	$8, 472(%rsp)
	jne	.LBB1_9
	movq	%r12, 184(%rsp)
	movq	448(%rsp), %rbx
	movq	480(%rsp), %rax
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 288(%rsp)
	vmovups	%ymm0, 320(%rsp)
	movq	$0, 352(%rsp)
	movq	%rax, 72(%rsp)
	movq	%rbx, 40(%rsp)
	movq	%r13, 16(%rsp)
	movq	%rbp, 8(%rsp)
	movq	%r15, (%rsp)
	movabsq	$_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
	leaq	288(%rsp), %rdi
	leaq	104(%rsp), %rsi
	movq	%r14, %rdx
	vzeroupper
	callq	*%rax
	movl	%eax, %ebp
	movq	104(%rsp), %r15
	movq	288(%rsp), %rax
	movq	%rax, 144(%rsp)
	movq	296(%rsp), %rax
	movq	%rax, 136(%rsp)
	movq	304(%rsp), %rax
	movq	%rax, 128(%rsp)
	movq	312(%rsp), %rax
	movq	%rax, 176(%rsp)
	movq	320(%rsp), %rax
	movq	%rax, 168(%rsp)
	movq	328(%rsp), %rax
	movq	%rax, 160(%rsp)
	movq	%r14, %rdi
	movq	336(%rsp), %rax
	movq	%rax, 152(%rsp)
	movq	344(%rsp), %r13
	movq	352(%rsp), %r14
	movabsq	$NRT_decref, %r12
	callq	*%r12
	movq	%rbx, %rdi
	callq	*%r12
	testl	%ebp, %ebp
	je	.LBB1_11
	movabsq	$PyErr_Clear, %rax
	callq	*%rax
	movl	8(%r15), %esi
	movq	(%r15), %rdi
	cmpl	$0, 32(%r15)
	jle	.LBB1_18
	movslq	%esi, %rsi
	movabsq	$PyBytes_FromStringAndSize, %rax
	callq	*%rax
	movq	%rax, %rbx
	movq	16(%r15), %rdi
	callq	*24(%r15)
	testq	%rax, %rax
	je	.LBB1_17
	movabsq	$numba_runtime_build_excinfo_struct, %rcx
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	*%rcx
	movq	%rax, %rbx
	movabsq	$NRT_Free, %rax
	movq	%r15, %rdi
	callq	*%rax
	testq	%rbx, %rbx
	jne	.LBB1_20
	jmp	.LBB1_22
.LBB1_11:
	movq	%r14, 112(%rsp)
	movq	%r13, 120(%rsp)
	movq	128(%rsp), %r14
	movq	136(%rsp), %rbp
	movq	144(%rsp), %rbx
	movq	184(%rsp), %rax
	movq	24(%rax), %rdi
	testq	%rdi, %rdi
	je	.LBB1_13
	movabsq	$PyList_GetItem, %rax
	xorl	%esi, %esi
	callq	*%rax
	movq	%rax, %r13
	jmp	.LBB1_14
.LBB1_18:
	movq	16(%r15), %rdx
	movabsq	$numba_unpickle, %rax
	callq	*%rax
	movq	%rax, %rbx
	testq	%rbx, %rbx
	je	.LBB1_22
.LBB1_20:
	movabsq	$numba_do_raise, %rax
	movq	%rbx, %rdi
.LBB1_21:
	callq	*%rax
.LBB1_22:
	xorl	%r14d, %r14d
	jmp	.LBB1_23
.LBB1_13:
	movabsq	$PyExc_RuntimeError, %rdi
	movabsq	$".const.`env.consts` is NULL in `read_const`", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	xorl	%r13d, %r13d
.LBB1_14:
	movabsq	$.const.pickledata.139799574043104, %rdi
	movabsq	$.const.pickledata.139799574043104.sha1, %rdx
	movabsq	$numba_unpickle, %rax
	movl	$32, %esi
	callq	*%rax
	movq	%rbx, 208(%rsp)
	movq	%rbp, 216(%rsp)
	movq	%r14, 224(%rsp)
	movq	176(%rsp), %rcx
	movq	%rcx, 232(%rsp)
	movq	168(%rsp), %rcx
	movq	%rcx, 240(%rsp)
	movq	160(%rsp), %rcx
	movq	%rcx, 248(%rsp)
	movq	152(%rsp), %rcx
	movq	%rcx, 256(%rsp)
	movq	120(%rsp), %rcx
	movq	%rcx, 264(%rsp)
	movq	112(%rsp), %rcx
	movq	%rcx, 272(%rsp)
	movabsq	$NRT_adapt_ndarray_to_python_acqref, %r9
	leaq	208(%rsp), %rdi
	movq	%rax, %rsi
	movl	$2, %edx
	movl	$1, %ecx
	movq	%r13, %r8
	callq	*%r9
	movq	%rax, %r14
	movq	%rbx, %rdi
	callq	*%r12
.LBB1_23:
	movq	%r14, %rax
	addq	$504, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	vzeroupper
	retq
.LBB1_2:
	.cfi_def_cfa_offset 560
	movabsq	$PyExc_RuntimeError, %rdi
	movabsq	$".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", %rsi
	jmp	.LBB1_3
.LBB1_5:
	movabsq	$PyExc_TypeError, %rdi
	movabsq	$".const.can't unbox array from PyObject into native value.  The object maybe of a different type", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	testb	%bpl, %bpl
	je	.LBB1_7
	jmp	.LBB1_22
.LBB1_9:
	movabsq	$PyExc_TypeError, %rdi
	movabsq	$".const.can't unbox array from PyObject into native value.  The object maybe of a different type", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	movabsq	$NRT_decref, %rax
	movq	%r14, %rdi
	jmp	.LBB1_21
.LBB1_17:
	movabsq	$PyExc_RuntimeError, %rdi
	movabsq	$".const.Error creating Python tuple from runtime exception arguments", %rsi
.LBB1_3:
	movabsq	$PyErr_SetString, %rax
	vzeroupper
	callq	*%rax
	jmp	.LBB1_22
.Lfunc_end1:
	.size	_ZN7cpython8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end1-_ZN7cpython8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	cfunc._ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	cfunc._ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
cfunc._ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$232, %rsp
	.cfi_def_cfa_offset 288
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rsi, %rdx
	movq	%rdi, %rbx
	vmovaps	288(%rsp), %xmm0
	movq	320(%rsp), %rax
	movq	352(%rsp), %rcx
	vxorps	%xmm1, %xmm1, %xmm1
	vmovups	%ymm1, 192(%rsp)
	vmovups	%ymm1, 160(%rsp)
	movq	$0, 224(%rsp)
	movq	$0, 104(%rsp)
	movq	%rcx, 72(%rsp)
	movq	%rax, 40(%rsp)
	vmovups	%xmm0, 8(%rsp)
	movq	%r9, (%rsp)
	movabsq	$_ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
	leaq	160(%rsp), %rdi
	leaq	104(%rsp), %rsi
	vzeroupper
	callq	*%rax
	movq	104(%rsp), %r14
	movq	160(%rsp), %rcx
	movq	168(%rsp), %rdx
	movq	176(%rsp), %rsi
	movq	184(%rsp), %rdi
	movq	192(%rsp), %r8
	movq	200(%rsp), %r9
	movq	208(%rsp), %r12
	movq	216(%rsp), %r13
	movq	224(%rsp), %rbp
	movl	$0, 100(%rsp)
	testl	%eax, %eax
	je	.LBB2_5
	movq	%r9, 112(%rsp)
	movq	%r8, 120(%rsp)
	movq	%rdi, 128(%rsp)
	movq	%rsi, 136(%rsp)
	movq	%rdx, 144(%rsp)
	movq	%rcx, 152(%rsp)
	movabsq	$numba_gil_ensure, %rax
	leaq	100(%rsp), %rdi
	callq	*%rax
	movabsq	$PyErr_Clear, %rax
	callq	*%rax
	movl	8(%r14), %esi
	movq	(%r14), %rdi
	cmpl	$0, 32(%r14)
	jle	.LBB2_6
	movslq	%esi, %rsi
	movabsq	$PyBytes_FromStringAndSize, %rax
	callq	*%rax
	movq	%rax, %r15
	movq	16(%r14), %rdi
	callq	*24(%r14)
	testq	%rax, %rax
	je	.LBB2_3
	movabsq	$numba_runtime_build_excinfo_struct, %rcx
	movq	%r15, %rdi
	movq	%rax, %rsi
	callq	*%rcx
	movq	%rax, %r15
	movabsq	$NRT_Free, %rax
	movq	%r14, %rdi
	callq	*%rax
	testq	%r15, %r15
	je	.LBB2_4
.LBB2_8:
	movabsq	$numba_do_raise, %rax
	movq	%r15, %rdi
	callq	*%rax
.LBB2_4:
	movabsq	$".const.<numba.core.cpu.CPUContext object at 0x7f2579141390>", %rdi
	movabsq	$PyUnicode_FromString, %rax
	callq	*%rax
	movq	%rax, %r14
	movabsq	$PyErr_WriteUnraisable, %rax
	movq	%r14, %rdi
	callq	*%rax
	movabsq	$Py_DecRef, %rax
	movq	%r14, %rdi
	callq	*%rax
	movabsq	$numba_gil_release, %rax
	leaq	100(%rsp), %rdi
	callq	*%rax
	movq	152(%rsp), %rcx
	movq	144(%rsp), %rdx
	movq	136(%rsp), %rsi
	movq	128(%rsp), %rdi
	movq	120(%rsp), %r8
	movq	112(%rsp), %r9
.LBB2_5:
	movq	%rcx, (%rbx)
	movq	%rdx, 8(%rbx)
	movq	%rsi, 16(%rbx)
	movq	%rdi, 24(%rbx)
	movq	%r8, 32(%rbx)
	movq	%r9, 40(%rbx)
	movq	%r12, 48(%rbx)
	movq	%r13, 56(%rbx)
	movq	%rbp, 64(%rbx)
	movq	%rbx, %rax
	addq	$232, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.LBB2_6:
	.cfi_def_cfa_offset 288
	movq	16(%r14), %rdx
	movabsq	$numba_unpickle, %rax
	callq	*%rax
	movq	%rax, %r15
	testq	%r15, %r15
	jne	.LBB2_8
	jmp	.LBB2_4
.LBB2_3:
	movabsq	$PyExc_RuntimeError, %rdi
	movabsq	$".const.Error creating Python tuple from runtime exception arguments.1", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	xorl	%ecx, %ecx
	xorl	%edx, %edx
	xorl	%esi, %esi
	xorl	%edi, %edi
	xorl	%r8d, %r8d
	xorl	%r9d, %r9d
	xorl	%r12d, %r12d
	xorl	%r13d, %r13d
	xorl	%ebp, %ebp
	jmp	.LBB2_5
.Lfunc_end2:
	.size	cfunc._ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end2-cfunc._ZN8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.weak	NRT_incref
	.p2align	4
	.type	NRT_incref,@function
NRT_incref:
	testq	%rdi, %rdi
	je	.LBB3_2
	lock		incq	(%rdi)
.LBB3_2:
	retq
.Lfunc_end3:
	.size	NRT_incref, .Lfunc_end3-NRT_incref

	.weak	NRT_decref
	.p2align	4
	.type	NRT_decref,@function
NRT_decref:
	.cfi_startproc
	testq	%rdi, %rdi
	je	.LBB4_2
	#MEMBARRIER
	lock		decq	(%rdi)
	je	.LBB4_3
.LBB4_2:
	retq
.LBB4_3:
	#MEMBARRIER
	movabsq	$NRT_MemInfo_call_dtor, %rax
	jmpq	*%rax
.Lfunc_end4:
	.size	NRT_decref, .Lfunc_end4-NRT_decref
	.cfi_endproc

	.type	".const.main.<locals>.nb_fused_blocked",@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
".const.main.<locals>.nb_fused_blocked":
	.asciz	"main.<locals>.nb_fused_blocked"
	.size	".const.main.<locals>.nb_fused_blocked", 31

	.type	_ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,8,8
	.type	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE",@object
	.p2align	4, 0x0
".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE":
	.asciz	"missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE"
	.size	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e16nb_fused_blockedB2v7B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", 189

	.type	".const.can't unbox array from PyObject into native value.  The object maybe of a different type",@object
	.p2align	4, 0x0
".const.can't unbox array from PyObject into native value.  The object maybe of a different type":
	.asciz	"can't unbox array from PyObject into native value.  The object maybe of a different type"
	.size	".const.can't unbox array from PyObject into native value.  The object maybe of a different type", 89

	.type	".const.`env.consts` is NULL in `read_const`",@object
	.p2align	4, 0x0
".const.`env.consts` is NULL in `read_const`":
	.asciz	"`env.consts` is NULL in `read_const`"
	.size	".const.`env.consts` is NULL in `read_const`", 37

	.type	.const.pickledata.139799574043104,@object
	.p2align	4, 0x0
.const.pickledata.139799574043104:
	.ascii	"\200\004\225\025\000\000\000\000\000\000\000\214\005numpy\224\214\007ndarray\224\223\224."
	.size	.const.pickledata.139799574043104, 32

	.type	.const.pickledata.139799574043104.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139799574043104.sha1:
	.ascii	"\337\274\375\323\237\313&\364\320\306\200\225D\207\270\300\265;\270\243"
	.size	.const.pickledata.139799574043104.sha1, 20

	.type	".const.Error creating Python tuple from runtime exception arguments",@object
	.p2align	4, 0x0
".const.Error creating Python tuple from runtime exception arguments":
	.asciz	"Error creating Python tuple from runtime exception arguments"
	.size	".const.Error creating Python tuple from runtime exception arguments", 61

	.type	".const.Error creating Python tuple from runtime exception arguments.1",@object
	.p2align	4, 0x0
".const.Error creating Python tuple from runtime exception arguments.1":
	.asciz	"Error creating Python tuple from runtime exception arguments"
	.size	".const.Error creating Python tuple from runtime exception arguments.1", 61

	.type	".const.<numba.core.cpu.CPUContext object at 0x7f2579141390>",@object
	.p2align	4, 0x0
".const.<numba.core.cpu.CPUContext object at 0x7f2579141390>":
	.asciz	"<numba.core.cpu.CPUContext object at 0x7f2579141390>"
	.size	".const.<numba.core.cpu.CPUContext object at 0x7f2579141390>", 53

	.type	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_zeros12_3clocals_3e4implB2v2B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE48omitted_28default_3d_3cclass_20_27float_27_3e_29,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_zeros12_3clocals_3e4implB2v2B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE48omitted_28default_3d_3cclass_20_27float_27_3e_29,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB2v3B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE39Function_28_3cclass_20_27float_27_3e_29,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB2v3B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE39Function_28_3cclass_20_27float_27_3e_29,8,8
	.type	.const.pickledata.139798927552384,@object
	.p2align	4, 0x0
.const.pickledata.139798927552384:
	.ascii	"\200\004\225B\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214\037negative dimensions not allowed\224\205\224N\207\224."
	.size	.const.pickledata.139798927552384, 77

	.type	.const.pickledata.139798927552384.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798927552384.sha1:
	.ascii	"3\033\205c\275\271\332\310\0338B\"s\005,Ho\301pk"
	.size	.const.pickledata.139798927552384.sha1, 20

	.type	.const.picklebuf.139798927552384,@object
	.p2align	4, 0x0
.const.picklebuf.139798927552384:
	.quad	.const.pickledata.139798927552384
	.long	77
	.zero	4
	.quad	.const.pickledata.139798927552384.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927552384, 40

	.type	.const.pickledata.139798927689024,@object
	.p2align	4, 0x0
.const.pickledata.139798927689024:
	.ascii	"\200\004\225~\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214[array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.\224\205\224N\207\224."
	.size	.const.pickledata.139798927689024, 137

	.type	.const.pickledata.139798927689024.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798927689024.sha1:
	.ascii	"X\341N\314\265\007\261\340 i\201t\002#\346\205\313\214<W"
	.size	.const.pickledata.139798927689024.sha1, 20

	.type	.const.picklebuf.139798927689024,@object
	.p2align	4, 0x0
.const.picklebuf.139798927689024:
	.quad	.const.pickledata.139798927689024
	.long	137
	.zero	4
	.quad	.const.pickledata.139798927689024.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927689024, 40

	.type	_ZN08NumbaEnv5numba2np8arrayobj15_call_allocatorB2v4B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj15_call_allocatorB2v4B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj18_ol_array_allocate12_3clocals_3e4implB2v5B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj18_ol_array_allocate12_3clocals_3e4implB2v5B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,8,8
	.type	.const.pickledata.139798927748736,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736:
	.ascii	"\200\004\225K\000\000\000\000\000\000\000\214\bbuiltins\224\214\013MemoryError\224\223\224\214'Allocation failed (probably too large).\224\205\224N\207\224."
	.size	.const.pickledata.139798927748736, 86

	.type	.const.pickledata.139798927748736.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736.sha1:
	.ascii	"\272(\235\201\360\\p \363G|\025sH\004\337e\253\342\t"
	.size	.const.pickledata.139798927748736.sha1, 20

	.type	.const.picklebuf.139798927748736,@object
	.p2align	4, 0x0
.const.picklebuf.139798927748736:
	.quad	.const.pickledata.139798927748736
	.long	86
	.zero	4
	.quad	.const.pickledata.139798927748736.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927748736, 40

	.type	_ZN08NumbaEnv5numba2np8arrayobj18ol_array_zero_fill12_3clocals_3e4implB2v6B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj18ol_array_zero_fill12_3clocals_3e4implB2v6B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.section	".note.GNU-stack","",@progbits
