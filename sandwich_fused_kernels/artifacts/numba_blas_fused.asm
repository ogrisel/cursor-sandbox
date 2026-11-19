	.file	"<string>"
	.section	.ltext,"axl",@progbits
	.globl	_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	subq	$408, %rsp
	.cfi_def_cfa_offset 464
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%r9, 232(%rsp)
	movq	%r8, 240(%rsp)
	movq	%rcx, 248(%rsp)
	movq	%rsi, 176(%rsp)
	movq	%rdi, 224(%rsp)
	movq	528(%rsp), %r14
	movq	520(%rsp), %r15
	movq	504(%rsp), %r12
	movq	552(%rsp), %rbp
	movq	512(%rsp), %rbx
	vxorps	%xmm0, %xmm0, %xmm0
	vmovaps	%xmm0, 320(%rsp)
	movq	480(%rsp), %rax
	movq	%rax, 160(%rsp)
	movabsq	$NRT_incref, %r13
	movq	%rdx, 256(%rsp)
	movq	%rdx, %rdi
	callq	*%r13
	movq	%r12, %rdi
	callq	*%r13
	movq	%r12, 264(%rsp)
	movq	%rbx, 272(%rsp)
	movq	%r15, 280(%rsp)
	movq	%r14, 288(%rsp)
	vmovupd	536(%rsp), %xmm0
	vmovupd	%xmm0, 296(%rsp)
	movq	%rbp, 312(%rsp)
	movq	$-1, 136(%rsp)
	movq	$1, 144(%rsp)
	movl	$1, %edx
	leaq	136(%rsp), %rdi
	xorl	%eax, %eax
	movl	$1, %esi
	xorl	%ecx, %ecx
	xorl	%r8d, %r8d
	.p2align	4
.LBB0_1:
	movq	(%rdi), %r9
	testq	%r9, %r9
	cmovsq	%r8, %rcx
	leaq	1(%r8), %r10
	movq	%r9, %r8
	cmovsq	%rdx, %r8
	imulq	%r8, %rsi
	shrq	$63, %r9
	addq	%r9, %rax
	addq	$8, %rdi
	movq	%r10, %r8
	cmpq	$2, %r10
	jne	.LBB0_1
	cmpq	$1, %rax
	je	.LBB0_6
	testq	%rax, %rax
	jne	.LBB0_13
	vcvtusi2sd	%r15, %xmm1, %xmm0
	vcvtsi2sd	%rsi, %xmm1, %xmm1
	vucomisd	%xmm1, %xmm0
	jne	.LBB0_5
	jnp	.LBB0_21
.LBB0_5:
	movabsq	$.const.picklebuf.139798921910016, %rax
	jmp	.LBB0_28
.LBB0_6:
	testq	%rsi, %rsi
	je	.LBB0_17
	movabsq	$9223372036854775792, %rax
	addq	$16, %rax
	cmpq	%rax, %r15
	jne	.LBB0_9
	cmpq	$-1, %rsi
	je	.LBB0_19
.LBB0_9:
	movq	%rsi, %rax
	orq	%r15, %rax
	shrq	$32, %rax
	testq	%rax, %rax
	je	.LBB0_14
	je	.LBB0_14
	je	.LBB0_14
	movq	%r15, %rax
	cqto
	idivq	%rsi
	jmp	.LBB0_15
.LBB0_13:
	movabsq	$.const.picklebuf.139798927836096, %rax
	jmp	.LBB0_28
.LBB0_14:
	movl	%r15d, %eax
	xorl	%edx, %edx
	divl	%esi
.LBB0_15:
	movq	%rdx, %rdi
	xorq	%rsi, %rdi
	sets	%r8b
	testq	%rdx, %rdx
	setne	%dil
	xorl	%r9d, %r9d
	andb	%r8b, %dil
	cmovneq	%rsi, %r9
	addq	%rdx, %r9
	jne	.LBB0_18
	movzbl	%dil, %edx
	subq	%rdx, %rax
	jmp	.LBB0_20
.LBB0_17:
	testq	%r15, %r15
	je	.LBB0_19
.LBB0_18:
	movabsq	$.const.picklebuf.139798920522816, %rax
	jmp	.LBB0_28
.LBB0_19:
	xorl	%eax, %eax
.LBB0_20:
	movq	%rax, 136(%rsp,%rcx,8)
.LBB0_21:
	movabsq	$numba_attempt_nocopy_reshape, %rax
	leaq	136(%rsp), %r8
	leaq	320(%rsp), %r9
	movl	$1, %edi
	movl	$2, %ecx
	leaq	304(%rsp), %rsi
	leaq	312(%rsp), %rdx
	pushq	$0
	.cfi_adjust_cfa_offset 8
	pushq	%r14
	.cfi_adjust_cfa_offset 8
	callq	*%rax
	addq	$16, %rsp
	.cfi_adjust_cfa_offset -16
	testl	%eax, %eax
	je	.LBB0_27
	movq	264(%rsp), %r14
	movq	296(%rsp), %r15
	movq	136(%rsp), %rbx
	movq	144(%rsp), %r13
	movq	%r14, %rdi
	movabsq	$NRT_incref, %rax
	callq	*%rax
	movabsq	$NRT_decref, %rax
	movq	%r12, %rdi
	callq	*%rax
	movq	472(%rsp), %rax
	movq	%rax, (%rsp)
	cmpq	$1, %rbx
	movq	480(%rsp), %rsi
	je	.LBB0_24
	movq	472(%rsp), %rcx
	cmpq	%rbx, %rcx
	setne	%al
	cmpq	$1, %rcx
	setne	%cl
	movq	%rbx, (%rsp)
	testb	%al, %cl
	jne	.LBB0_26
.LBB0_24:
	movq	160(%rsp), %r12
	cmpq	$1, %r13
	je	.LBB0_31
	cmpq	%r13, %rsi
	setne	%al
	cmpq	$1, %rsi
	setne	%cl
	movq	%r13, %r12
	testb	%al, %cl
	je	.LBB0_31
.LBB0_26:
	movabsq	$.const.picklebuf.139798919238336, %rax
	jmp	.LBB0_28
.LBB0_27:
	movabsq	$.const.picklebuf.139798928103424, %rax
.LBB0_28:
	movq	176(%rsp), %rcx
	movq	%rax, (%rcx)
.LBB0_29:
	movl	$1, %r15d
.LBB0_30:
	movl	%r15d, %eax
	addq	$408, %rsp
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
.LBB0_31:
	.cfi_def_cfa_offset 464
	movq	%r13, 16(%rsp)
	movq	(%rsp), %r13
	imulq	%r12, %r13
	jo	.LBB0_330
	movabsq	$-1152921504606846976, %rax
	addq	%r13, %rax
	shrq	$61, %rax
	cmpl	$7, %eax
	jb	.LBB0_330
	leaq	(,%r13,8), %rdi
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	movl	$32, %esi
	callq	*%rax
	testq	%rax, %rax
	je	.LBB0_331
	movq	%r13, 112(%rsp)
	movq	%r14, 152(%rsp)
	movq	%r12, 32(%rsp)
	leaq	(,%r12,8), %rcx
	movq	%rcx, 8(%rsp)
	movq	%rax, 216(%rsp)
	movq	24(%rax), %rax
	movq	%rax, 80(%rsp)
	cmpq	$0, (%rsp)
	movq	16(%rsp), %rcx
	jle	.LBB0_327
	cmpq	$0, 32(%rsp)
	jle	.LBB0_327
	cmpq	$2, %rbx
	jb	.LBB0_72
	movq	112(%rsp), %rax
	movq	80(%rsp), %r13
	leaq	(%r13,%rax,8), %rax
	movq	%rax, 24(%rsp)
	cmpq	$2, %rcx
	movq	464(%rsp), %r14
	movq	32(%rsp), %r9
	movq	480(%rsp), %rdi
	jb	.LBB0_90
	cmpq	$2, 472(%rsp)
	jb	.LBB0_162
	movq	(%rsp), %rax
	decq	%rax
	movq	16(%rsp), %rbp
	movq	%rbp, %rcx
	imulq	%rax, %rcx
	addq	%r9, %rcx
	leaq	(%r15,%rcx,8), %rcx
	imulq	%rdi, %rax
	addq	%r9, %rax
	leaq	(%r14,%rax,8), %rax
	movq	24(%rsp), %r8
	cmpq	%r8, %r15
	setb	%dl
	leaq	(,%rdi,8), %rsi
	movq	%rsi, 64(%rsp)
	cmpq	%rcx, %r13
	setb	%cl
	andb	%cl, %dl
	movq	%rbp, %rsi
	orq	%r9, %rsi
	shrq	$60, %rsi
	andl	$1, %esi
	orb	%dl, %sil
	movq	%rsi, 104(%rsp)
	movabsq	$8070450532247928816, %rdx
	movq	%r9, %rsi
	andq	%rdx, %rsi
	movq	%rsi, 120(%rsp)
	orq	$12, %rdx
	andq	%r9, %rdx
	movq	%rdx, 128(%rsp)
	cmpq	%r8, %r15
	setb	%dl
	andb	%cl, %dl
	cmpq	$0, 8(%rsp)
	sets	%cl
	movq	%rbp, %rsi
	shrq	$60, %rsi
	andl	$1, %esi
	orb	%cl, %sil
	orb	%dl, %sil
	cmpq	%rax, %r13
	setb	%al
	cmpq	%r8, %r14
	setb	%dl
	leaq	8(%r14), %r8
	movq	%r8, 96(%rsp)
	andb	%al, %dl
	shrq	$60, %rdi
	andl	$1, %edi
	orb	%cl, %dil
	orb	%dl, %dil
	orb	%sil, %dil
	movq	%rdi, 72(%rsp)
	movabsq	$9223372036854775792, %r10
	andq	%r9, %r10
	leaq	-1(%r10), %rax
	movq	%rax, 88(%rsp)
	movl	%r9d, %r8d
	andl	$7, %r8d
	leaq	96(%r15), %r11
	shlq	$3, %rbp
	leaq	96(%r13), %rax
	leaq	96(%r14), %rdx
	negq	%r9
	xorl	%r12d, %r12d
	movq	%r14, %rbx
	movq	%r13, %rcx
	xorl	%r14d, %r14d
	movq	%rbp, 16(%rsp)
	jmp	.LBB0_42
.LBB0_40:
	movq	16(%rsp), %rbp
.LBB0_41:
	incq	%r12
	addq	%rbp, %r11
	movq	8(%rsp), %rsi
	addq	%rsi, %rax
	addq	%rbp, %r15
	addq	%rsi, %rcx
	movq	64(%rsp), %rsi
	addq	%rsi, %rdx
	addq	%rsi, %rbx
	cmpq	(%rsp), %r12
	je	.LBB0_327
.LBB0_42:
	movq	480(%rsp), %rdi
	cmpq	$2, %rdi
	jb	.LBB0_45
	movq	32(%rsp), %rdi
	cmpq	$16, %rdi
	setb	%sil
	orb	72(%rsp), %sil
	testb	$1, %sil
	je	.LBB0_53
	xorl	%esi, %esi
	jmp	.LBB0_56
.LBB0_45:
	movq	%r12, %rsi
	imulq	%rdi, %rsi
	movq	464(%rsp), %rdi
	leaq	(%rdi,%rsi,8), %rsi
	leaq	(%rsi,%r14,8), %rbp
	movq	32(%rsp), %r13
	cmpq	$3, %r13
	jbe	.LBB0_47
	movq	64(%rsp), %rsi
	imulq	%r12, %rsi
	addq	96(%rsp), %rsi
	leaq	(%rsi,%r14,8), %rsi
	cmpq	%rsi, 80(%rsp)
	setb	%sil
	cmpq	24(%rsp), %rbp
	setb	%dil
	andb	%sil, %dil
	orb	104(%rsp), %dil
	je	.LBB0_63
.LBB0_47:
	xorl	%esi, %esi
.LBB0_48:
	movl	%r13d, %edi
	subl	%esi, %edi
	movq	%rsi, %r13
	andl	$7, %edi
	je	.LBB0_51
	movq	%rsi, %r13
	.p2align	4
.LBB0_50:
	vmovsd	(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, (%rcx,%r13,8)
	incq	%r13
	decq	%rdi
	jne	.LBB0_50
.LBB0_51:
	movq	32(%rsp), %rdi
	subq	%rdi, %rsi
	cmpq	$-8, %rsi
	ja	.LBB0_40
	.p2align	4
.LBB0_52:
	vmovsd	(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, (%rcx,%r13,8)
	vmovsd	8(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%rcx,%r13,8)
	vmovsd	16(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%rcx,%r13,8)
	vmovsd	24(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%rcx,%r13,8)
	vmovsd	32(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%rcx,%r13,8)
	vmovsd	40(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%rcx,%r13,8)
	vmovsd	48(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%rcx,%r13,8)
	vmovsd	56(%r15,%r13,8), %xmm0
	vmulsd	(%rbp), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%rcx,%r13,8)
	addq	$8, %r13
	cmpq	%r13, %rdi
	jne	.LBB0_52
	jmp	.LBB0_40
.LBB0_53:
	xorl	%esi, %esi
	.p2align	4
.LBB0_54:
	vmovupd	-96(%r11,%rsi,8), %ymm0
	vmovupd	-64(%r11,%rsi,8), %ymm1
	vmovupd	-32(%r11,%rsi,8), %ymm2
	vmovupd	(%r11,%rsi,8), %ymm3
	vmulpd	-96(%rdx,%rsi,8), %ymm0, %ymm0
	vmulpd	-64(%rdx,%rsi,8), %ymm1, %ymm1
	vmulpd	-32(%rdx,%rsi,8), %ymm2, %ymm2
	vmulpd	(%rdx,%rsi,8), %ymm3, %ymm3
	vmovupd	%ymm0, -96(%rax,%rsi,8)
	vmovupd	%ymm1, -64(%rax,%rsi,8)
	vmovupd	%ymm2, -32(%rax,%rsi,8)
	vmovupd	%ymm3, (%rax,%rsi,8)
	addq	$16, %rsi
	cmpq	%rsi, %r10
	jne	.LBB0_54
	movq	%r10, %rsi
	movq	88(%rsp), %r14
	cmpq	%r10, %rdi
	je	.LBB0_41
.LBB0_56:
	movq	%rsi, %rdi
	testq	%r8, %r8
	je	.LBB0_60
	leaq	(%rcx,%rsi,8), %rdi
	leaq	(%rbx,%rsi,8), %r14
	leaq	(%r15,%rsi,8), %rbp
	xorl	%r13d, %r13d
	.p2align	4
.LBB0_58:
	vmovsd	(%rbp,%r13,8), %xmm0
	vmulsd	(%r14,%r13,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%rdi,%r13,8)
	incq	%r13
	cmpq	%r13, %r8
	jne	.LBB0_58
	leaq	(%rsi,%r13), %rdi
	leaq	-1(%rsi,%r13), %r14
	movq	16(%rsp), %rbp
.LBB0_60:
	subq	32(%rsp), %rsi
	cmpq	$-8, %rsi
	ja	.LBB0_41
	decq	%rdi
	movq	%rdi, %r14
	.p2align	4
.LBB0_62:
	vmovsd	8(%r15,%r14,8), %xmm0
	vmulsd	8(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%rcx,%r14,8)
	vmovsd	16(%r15,%r14,8), %xmm0
	vmulsd	16(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%rcx,%r14,8)
	vmovsd	24(%r15,%r14,8), %xmm0
	vmulsd	24(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%rcx,%r14,8)
	vmovsd	32(%r15,%r14,8), %xmm0
	vmulsd	32(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%rcx,%r14,8)
	vmovsd	40(%r15,%r14,8), %xmm0
	vmulsd	40(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%rcx,%r14,8)
	vmovsd	48(%r15,%r14,8), %xmm0
	vmulsd	48(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%rcx,%r14,8)
	vmovsd	56(%r15,%r14,8), %xmm0
	vmulsd	56(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%rcx,%r14,8)
	vmovsd	64(%r15,%r14,8), %xmm0
	vmulsd	64(%rbx,%r14,8), %xmm0, %xmm0
	vmovsd	%xmm0, 64(%rcx,%r14,8)
	leaq	8(%r9,%r14), %rsi
	addq	$8, %r14
	cmpq	$-1, %rsi
	jne	.LBB0_62
	jmp	.LBB0_41
.LBB0_63:
	cmpq	$16, %r13
	jae	.LBB0_65
	xorl	%edi, %edi
	jmp	.LBB0_69
.LBB0_65:
	vbroadcastsd	(%rbp), %ymm0
	xorl	%esi, %esi
	movq	120(%rsp), %rdi
	.p2align	4
.LBB0_66:
	vmulpd	-96(%r11,%rsi,8), %ymm0, %ymm1
	vmulpd	-64(%r11,%rsi,8), %ymm0, %ymm2
	vmulpd	-32(%r11,%rsi,8), %ymm0, %ymm3
	vmulpd	(%r11,%rsi,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rax,%rsi,8)
	vmovupd	%ymm2, -64(%rax,%rsi,8)
	vmovupd	%ymm3, -32(%rax,%rsi,8)
	vmovupd	%ymm4, (%rax,%rsi,8)
	addq	$16, %rsi
	cmpq	%rsi, %rdi
	jne	.LBB0_66
	cmpq	%rdi, %r13
	je	.LBB0_40
	movq	%rdi, %rsi
	testb	$12, %r13b
	je	.LBB0_48
.LBB0_69:
	vbroadcastsd	(%rbp), %ymm0
	movq	128(%rsp), %rsi
	.p2align	4
.LBB0_70:
	vmulpd	(%r15,%rdi,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%rcx,%rdi,8)
	addq	$4, %rdi
	cmpq	%rdi, %rsi
	jne	.LBB0_70
	cmpq	%rsi, %r13
	je	.LBB0_40
	jmp	.LBB0_48
.LBB0_72:
	cmpq	$1, %rcx
	movq	464(%rsp), %rbp
	movq	32(%rsp), %r11
	movq	80(%rsp), %rbx
	movq	480(%rsp), %rdi
	jbe	.LBB0_126
	movabsq	$9223372036854775792, %rax
	cmpq	$2, 472(%rsp)
	jb	.LBB0_180
	movabsq	$2305843009213693951, %rdx
	addq	(%rsp), %rdx
	imulq	%rdi, %rdx
	movq	112(%rsp), %rcx
	leaq	(%rbx,%rcx,8), %rcx
	leaq	(%r15,%r11,8), %rsi
	cmpq	$1, %rdi
	jbe	.LBB0_237
	movq	%rdi, %r13
	addq	%r11, %rdx
	cmpq	%rsi, %rbx
	setb	%sil
	cmpq	%rcx, %r15
	setb	%dil
	leaq	(%rbp,%rdx,8), %rdx
	andb	%sil, %dil
	cmpq	%rdx, %rbx
	setb	%dl
	cmpq	%rcx, %rbp
	setb	%sil
	andb	%dl, %sil
	cmpq	$0, 8(%rsp)
	sets	%dl
	movq	%r13, %rcx
	shrq	$60, %rcx
	andl	$1, %ecx
	orb	%dl, %cl
	orb	%sil, %cl
	orb	%dil, %cl
	movq	%r11, %rdx
	andq	%rax, %rdx
	addq	$12, %rax
	andq	%r11, %rax
	leaq	96(%rbp), %rsi
	shlq	$3, %r13
	leaq	96(%rbx), %rdi
	xorl	%r8d, %r8d
	movq	%rbx, %r9
	movq	32(%rsp), %r12
	jmp	.LBB0_77
.LBB0_76:
	incq	%r8
	addq	%r13, %rsi
	movq	8(%rsp), %r11
	addq	%r11, %rdi
	addq	%r13, %rbp
	addq	%r11, %r9
	cmpq	(%rsp), %r8
	je	.LBB0_327
.LBB0_77:
	cmpq	$4, %r12
	setb	%r11b
	orb	%cl, %r11b
	testb	$1, %r11b
	je	.LBB0_79
	xorl	%ebx, %ebx
	jmp	.LBB0_85
.LBB0_79:
	xorl	%r11d, %r11d
	cmpq	$16, %r12
	jb	.LBB0_83
	.p2align	4
.LBB0_80:
	vmovupd	(%r15,%r11,8), %ymm0
	vmovupd	32(%r15,%r11,8), %ymm1
	vmovupd	64(%r15,%r11,8), %ymm2
	vmovupd	96(%r15,%r11,8), %ymm3
	vmulpd	-96(%rsi,%r11,8), %ymm0, %ymm0
	vmulpd	-64(%rsi,%r11,8), %ymm1, %ymm1
	vmulpd	-32(%rsi,%r11,8), %ymm2, %ymm2
	vmulpd	(%rsi,%r11,8), %ymm3, %ymm3
	vmovupd	%ymm0, -96(%rdi,%r11,8)
	vmovupd	%ymm1, -64(%rdi,%r11,8)
	vmovupd	%ymm2, -32(%rdi,%r11,8)
	vmovupd	%ymm3, (%rdi,%r11,8)
	addq	$16, %r11
	cmpq	%r11, %rdx
	jne	.LBB0_80
	cmpq	%rdx, %r12
	je	.LBB0_76
	movq	%rdx, %r11
	movq	%rdx, %rbx
	testb	$12, %r12b
	je	.LBB0_85
	.p2align	4
.LBB0_83:
	vmovupd	(%r15,%r11,8), %ymm0
	vmulpd	(%rbp,%r11,8), %ymm0, %ymm0
	vmovupd	%ymm0, (%r9,%r11,8)
	addq	$4, %r11
	cmpq	%r11, %rax
	jne	.LBB0_83
	movq	%rax, %rbx
	cmpq	%rax, %r12
	je	.LBB0_76
.LBB0_85:
	movl	%r12d, %r14d
	subl	%ebx, %r14d
	movq	%rbx, %r11
	andl	$7, %r14d
	je	.LBB0_88
	movq	%rbx, %r11
	.p2align	4
.LBB0_87:
	vmovsd	(%r15,%r11,8), %xmm0
	vmulsd	(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r11,8)
	incq	%r11
	decq	%r14
	jne	.LBB0_87
.LBB0_88:
	subq	%r12, %rbx
	cmpq	$-8, %rbx
	ja	.LBB0_76
	.p2align	4
.LBB0_89:
	vmovsd	(%r15,%r11,8), %xmm0
	vmulsd	(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r11,8)
	vmovsd	8(%r15,%r11,8), %xmm0
	vmulsd	8(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r9,%r11,8)
	vmovsd	16(%r15,%r11,8), %xmm0
	vmulsd	16(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r9,%r11,8)
	vmovsd	24(%r15,%r11,8), %xmm0
	vmulsd	24(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r9,%r11,8)
	vmovsd	32(%r15,%r11,8), %xmm0
	vmulsd	32(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r9,%r11,8)
	vmovsd	40(%r15,%r11,8), %xmm0
	vmulsd	40(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r9,%r11,8)
	vmovsd	48(%r15,%r11,8), %xmm0
	vmulsd	48(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r9,%r11,8)
	vmovsd	56(%r15,%r11,8), %xmm0
	vmulsd	56(%rbp,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r9,%r11,8)
	addq	$8, %r11
	cmpq	%r11, %r12
	jne	.LBB0_89
	jmp	.LBB0_76
.LBB0_90:
	cmpq	$2, 472(%rsp)
	jb	.LBB0_199
	movq	(%rsp), %rax
	decq	%rax
	movq	16(%rsp), %r8
	movq	%r8, %rcx
	imulq	%rax, %rcx
	leaq	8(%r15,%rcx,8), %rcx
	imulq	%rdi, %rax
	addq	%r9, %rax
	leaq	(%r14,%rax,8), %rax
	leaq	(,%rdi,8), %rdx
	movq	%rdx, 64(%rsp)
	leaq	8(%r14), %rdx
	movq	%rdx, 96(%rsp)
	movq	24(%rsp), %r10
	cmpq	%r10, %r15
	setb	%dl
	cmpq	%rcx, %r13
	setb	%sil
	andb	%sil, %dl
	movq	%r9, %rcx
	shrq	$60, %rcx
	andl	$1, %ecx
	orb	%dl, %cl
	movq	%rcx, 88(%rsp)
	movabsq	$8070450532247928816, %rcx
	movq	%r9, %rdx
	andq	%rcx, %rdx
	movq	%rdx, 120(%rsp)
	orq	$12, %rcx
	andq	%r9, %rcx
	cmpq	%r10, %r15
	setb	%dl
	andb	%sil, %dl
	cmpq	%rax, %r13
	setb	%al
	cmpq	%r10, %r14
	setb	%sil
	andb	%al, %sil
	orq	%r9, %rdi
	shrq	$60, %rdi
	andl	$1, %edi
	orb	%sil, %dil
	orb	%dl, %dil
	movq	%rdi, 104(%rsp)
	movabsq	$9223372036854775792, %rax
	andq	%r9, %rax
	leaq	-1(%rax), %rdx
	movq	%rdx, 128(%rsp)
	movl	%r9d, %edx
	andl	$7, %edx
	movq	%rdx, 72(%rsp)
	leaq	96(%r13), %rbx
	leaq	96(%r14), %r12
	movq	%r9, %rdx
	negq	%rdx
	xorl	%r10d, %r10d
	movq	%r13, %rsi
	movq	%r8, %r13
	xorl	%r11d, %r11d
	jmp	.LBB0_94
.LBB0_92:
	movq	16(%rsp), %r13
.LBB0_93:
	incq	%r10
	movq	8(%rsp), %rdi
	addq	%rdi, %rbx
	addq	%rdi, %rsi
	movq	64(%rsp), %rdi
	addq	%rdi, %r12
	addq	%rdi, %r14
	cmpq	(%rsp), %r10
	je	.LBB0_327
.LBB0_94:
	movq	%r10, %rbp
	imulq	%r13, %rbp
	movq	480(%rsp), %r8
	cmpq	$2, %r8
	jb	.LBB0_97
	movq	32(%rsp), %r8
	cmpq	$16, %r8
	setb	%dil
	orb	104(%rsp), %dil
	testb	$1, %dil
	je	.LBB0_99
	xorl	%edi, %edi
	jmp	.LBB0_102
.LBB0_97:
	movq	%r10, %rdi
	imulq	%r8, %rdi
	movq	464(%rsp), %r8
	leaq	(%r8,%rdi,8), %rdi
	leaq	(%rdi,%r11,8), %r9
	movq	32(%rsp), %r13
	cmpq	$4, %r13
	jb	.LBB0_98
	movq	64(%rsp), %rdi
	imulq	%r10, %rdi
	addq	96(%rsp), %rdi
	leaq	(%rdi,%r11,8), %rdi
	cmpq	%rdi, 80(%rsp)
	setb	%dil
	cmpq	24(%rsp), %r9
	setb	%r8b
	andb	%dil, %r8b
	orb	88(%rsp), %r8b
	je	.LBB0_111
.LBB0_98:
	xorl	%edi, %edi
.LBB0_120:
	movl	%r13d, %r8d
	subl	%edi, %r8d
	movq	%rdi, %r13
	andl	$7, %r8d
	je	.LBB0_123
	movq	%rdi, %r13
	.p2align	4
.LBB0_122:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, (%rsi,%r13,8)
	incq	%r13
	decq	%r8
	jne	.LBB0_122
.LBB0_123:
	subq	32(%rsp), %rdi
	cmpq	$-8, %rdi
	ja	.LBB0_92
	movq	32(%rsp), %rdi
	.p2align	4
.LBB0_125:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, (%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%rsi,%r13,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%rsi,%r13,8)
	addq	$8, %r13
	cmpq	%r13, %rdi
	jne	.LBB0_125
	jmp	.LBB0_92
.LBB0_99:
	vbroadcastsd	(%r15,%rbp,8), %ymm0
	xorl	%edi, %edi
	.p2align	4
.LBB0_100:
	vmulpd	-96(%r12,%rdi,8), %ymm0, %ymm1
	vmulpd	-64(%r12,%rdi,8), %ymm0, %ymm2
	vmulpd	-32(%r12,%rdi,8), %ymm0, %ymm3
	vmulpd	(%r12,%rdi,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rbx,%rdi,8)
	vmovupd	%ymm2, -64(%rbx,%rdi,8)
	vmovupd	%ymm3, -32(%rbx,%rdi,8)
	vmovupd	%ymm4, (%rbx,%rdi,8)
	addq	$16, %rdi
	cmpq	%rdi, %rax
	jne	.LBB0_100
	movq	%rax, %rdi
	movq	128(%rsp), %r11
	cmpq	%rax, %r8
	je	.LBB0_93
.LBB0_102:
	movq	%rdi, %r9
	cmpq	$0, 72(%rsp)
	movq	32(%rsp), %r13
	je	.LBB0_106
	movq	72(%rsp), %r8
	movq	%rdi, %r9
	.p2align	4
.LBB0_104:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%rsi,%r9,8)
	incq	%r9
	decq	%r8
	jne	.LBB0_104
	leaq	-1(%r9), %r11
.LBB0_106:
	subq	%r13, %rdi
	cmpq	$-8, %rdi
	movq	16(%rsp), %r13
	ja	.LBB0_93
	decq	%r9
	movq	%r9, %r11
	.p2align	4
.LBB0_108:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	8(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	16(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	24(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	32(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	40(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	48(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	56(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%rsi,%r11,8)
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	64(%r14,%r11,8), %xmm0, %xmm0
	vmovsd	%xmm0, 64(%rsi,%r11,8)
	leaq	8(%rdx,%r11), %rdi
	addq	$8, %r11
	cmpq	$-1, %rdi
	jne	.LBB0_108
	jmp	.LBB0_93
.LBB0_111:
	cmpq	$16, %r13
	jae	.LBB0_113
	xorl	%r8d, %r8d
	jmp	.LBB0_117
.LBB0_113:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	xorl	%edi, %edi
	movq	120(%rsp), %r8
	.p2align	4
.LBB0_114:
	vmovupd	%ymm0, -96(%rbx,%rdi,8)
	vmovupd	%ymm0, -64(%rbx,%rdi,8)
	vmovupd	%ymm0, -32(%rbx,%rdi,8)
	vmovupd	%ymm0, (%rbx,%rdi,8)
	addq	$16, %rdi
	cmpq	%rdi, %r8
	jne	.LBB0_114
	cmpq	%r8, %r13
	je	.LBB0_92
	movq	%r8, %rdi
	testb	$12, %r13b
	je	.LBB0_120
.LBB0_117:
	vmovsd	(%r15,%rbp,8), %xmm0
	vmulsd	(%r9), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	.p2align	4
.LBB0_118:
	vmovupd	%ymm0, (%rsi,%r8,8)
	addq	$4, %r8
	cmpq	%r8, %rcx
	jne	.LBB0_118
	movq	%rcx, %rdi
	cmpq	%rcx, %r13
	je	.LBB0_92
	jmp	.LBB0_120
.LBB0_126:
	movq	112(%rsp), %rax
	leaq	(%rbx,%rax,8), %rsi
	leaq	8(%r15), %rax
	cmpq	$2, 472(%rsp)
	jb	.LBB0_218
	movq	(%rsp), %rcx
	decq	%rcx
	imulq	%rdi, %rcx
	addq	%r11, %rcx
	leaq	(%rbp,%rcx,8), %rcx
	leaq	(,%rdi,8), %r14
	leaq	8(%rbp), %rdx
	movq	%rdx, 104(%rsp)
	cmpq	%rax, %rbx
	setb	%al
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	movq	%r11, %r8
	shrq	$60, %r8
	andl	$1, %r8d
	orb	%dl, %r8b
	movq	%r8, 96(%rsp)
	movabsq	$8070450532247928816, %r9
	movq	%r11, %r8
	andq	%r9, %r8
	orq	$12, %r9
	andq	%r11, %r9
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	cmpq	%rcx, %rbx
	setb	%al
	movq	%rsi, 72(%rsp)
	cmpq	%rsi, %rbp
	setb	%cl
	andb	%al, %cl
	orq	%r11, %rdi
	shrq	$60, %rdi
	andl	$1, %edi
	orb	%cl, %dil
	orb	%dl, %dil
	movq	%rdi, 64(%rsp)
	movabsq	$9223372036854775792, %r10
	andq	%r11, %r10
	leaq	-1(%r10), %rax
	movq	%rax, 88(%rsp)
	movl	%r11d, %eax
	andl	$7, %eax
	movq	%rax, 16(%rsp)
	leaq	96(%rbx), %r12
	movq	%r11, %rdx
	movq	%rbx, %r11
	movq	%r14, %rbx
	leaq	96(%rbp), %r13
	negq	%rdx
	xorl	%r14d, %r14d
	xorl	%eax, %eax
	movq	%rbx, 24(%rsp)
	jmp	.LBB0_130
.LBB0_128:
	movq	24(%rsp), %rbx
.LBB0_129:
	incq	%r14
	movq	8(%rsp), %rcx
	addq	%rcx, %r12
	addq	%rcx, %r11
	addq	%rbx, %r13
	addq	%rbx, %rbp
	cmpq	(%rsp), %r14
	je	.LBB0_327
.LBB0_130:
	movq	480(%rsp), %rsi
	cmpq	$2, %rsi
	jb	.LBB0_133
	cmpq	$16, 32(%rsp)
	setb	%al
	orb	64(%rsp), %al
	testb	$1, %al
	je	.LBB0_142
	xorl	%esi, %esi
	jmp	.LBB0_145
.LBB0_133:
	movq	%r14, %rcx
	imulq	%rsi, %rcx
	movq	464(%rsp), %rsi
	leaq	(%rsi,%rcx,8), %rcx
	leaq	(%rcx,%rax,8), %rsi
	cmpq	$3, 32(%rsp)
	jbe	.LBB0_135
	movq	%rbx, %rcx
	imulq	%r14, %rcx
	addq	104(%rsp), %rcx
	leaq	(%rcx,%rax,8), %rcx
	cmpq	%rcx, 80(%rsp)
	setb	%cl
	cmpq	72(%rsp), %rsi
	setb	%dil
	andb	%cl, %dil
	orb	96(%rsp), %dil
	je	.LBB0_152
.LBB0_135:
	xorl	%edi, %edi
.LBB0_136:
	movq	32(%rsp), %rcx
	subl	%edi, %ecx
	movq	%rdi, %rbx
	andl	$7, %ecx
	je	.LBB0_139
	movq	%rdi, %rbx
	.p2align	4
.LBB0_138:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, (%r11,%rbx,8)
	incq	%rbx
	decq	%rcx
	jne	.LBB0_138
.LBB0_139:
	movq	32(%rsp), %rcx
	subq	%rcx, %rdi
	cmpq	$-8, %rdi
	ja	.LBB0_128
	.p2align	4
.LBB0_140:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, (%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r11,%rbx,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r11,%rbx,8)
	addq	$8, %rbx
	cmpq	%rbx, %rcx
	jne	.LBB0_140
	jmp	.LBB0_128
.LBB0_142:
	vbroadcastsd	(%r15), %ymm0
	xorl	%eax, %eax
	.p2align	4
.LBB0_143:
	vmulpd	-96(%r13,%rax,8), %ymm0, %ymm1
	vmulpd	-64(%r13,%rax,8), %ymm0, %ymm2
	vmulpd	-32(%r13,%rax,8), %ymm0, %ymm3
	vmulpd	(%r13,%rax,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%r12,%rax,8)
	vmovupd	%ymm2, -64(%r12,%rax,8)
	vmovupd	%ymm3, -32(%r12,%rax,8)
	vmovupd	%ymm4, (%r12,%rax,8)
	addq	$16, %rax
	cmpq	%rax, %r10
	jne	.LBB0_143
	movq	%r10, %rsi
	movq	88(%rsp), %rax
	cmpq	%r10, 32(%rsp)
	je	.LBB0_129
.LBB0_145:
	movq	%rsi, %rdi
	cmpq	$0, 16(%rsp)
	je	.LBB0_149
	movq	16(%rsp), %rax
	movq	%rsi, %rdi
	.p2align	4
.LBB0_147:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbp,%rdi,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r11,%rdi,8)
	incq	%rdi
	decq	%rax
	jne	.LBB0_147
	leaq	-1(%rdi), %rax
.LBB0_149:
	subq	32(%rsp), %rsi
	cmpq	$-8, %rsi
	ja	.LBB0_129
	decq	%rdi
	movq	%rdi, %rax
	.p2align	4
.LBB0_151:
	vmovsd	(%r15), %xmm0
	vmulsd	8(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	16(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	24(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	32(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	40(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	48(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	56(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r11,%rax,8)
	vmovsd	(%r15), %xmm0
	vmulsd	64(%rbp,%rax,8), %xmm0, %xmm0
	vmovsd	%xmm0, 64(%r11,%rax,8)
	leaq	8(%rdx,%rax), %rcx
	addq	$8, %rax
	cmpq	$-1, %rcx
	jne	.LBB0_151
	jmp	.LBB0_129
.LBB0_152:
	cmpq	$16, 32(%rsp)
	jae	.LBB0_154
	xorl	%ecx, %ecx
	jmp	.LBB0_159
.LBB0_154:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	xorl	%ecx, %ecx
	.p2align	4
.LBB0_155:
	vmovupd	%ymm0, -96(%r12,%rcx,8)
	vmovupd	%ymm0, -64(%r12,%rcx,8)
	vmovupd	%ymm0, -32(%r12,%rcx,8)
	vmovupd	%ymm0, (%r12,%rcx,8)
	addq	$16, %rcx
	cmpq	%rcx, %r8
	jne	.LBB0_155
	movq	32(%rsp), %rbx
	cmpq	%r8, %rbx
	je	.LBB0_128
	movq	%r8, %rdi
	movq	%r8, %rcx
	testb	$12, %bl
	movq	24(%rsp), %rbx
	je	.LBB0_136
.LBB0_159:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rsi), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	.p2align	4
.LBB0_160:
	vmovupd	%ymm0, (%r11,%rcx,8)
	addq	$4, %rcx
	cmpq	%rcx, %r9
	jne	.LBB0_160
	movq	%r9, %rdi
	cmpq	%r9, 32(%rsp)
	je	.LBB0_129
	jmp	.LBB0_136
.LBB0_162:
	movabsq	$2305843009213693951, %rcx
	movabsq	$1152921504606846976, %rax
	cmpq	$1, %rdi
	jbe	.LBB0_255
	addq	(%rsp), %rcx
	movq	16(%rsp), %r10
	imulq	%r10, %rcx
	addq	%r9, %rcx
	leaq	(%r15,%rcx,8), %rcx
	leaq	(%r14,%r9,8), %rdx
	cmpq	%rcx, %r13
	setb	%cl
	movq	24(%rsp), %r8
	cmpq	%r8, %r15
	setb	%sil
	andb	%cl, %sil
	cmpq	$0, 8(%rsp)
	sets	%cl
	testq	%rax, %r10
	setne	%dil
	orb	%cl, %dil
	orb	%sil, %dil
	cmpq	%rdx, %r13
	setb	%cl
	cmpq	%r8, %r14
	setb	%al
	andb	%cl, %al
	orb	%dil, %al
	movabsq	$9223372036854775792, %rcx
	movq	%r9, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r9, %rcx
	leaq	96(%r15), %rsi
	shlq	$3, %r10
	leaq	96(%r13), %rdi
	xorl	%r8d, %r8d
	movq	%r13, %r9
	movq	%r10, %r13
	movq	32(%rsp), %r12
	jmp	.LBB0_165
.LBB0_164:
	incq	%r8
	addq	%r13, %rsi
	movq	8(%rsp), %r10
	addq	%r10, %rdi
	addq	%r13, %r15
	addq	%r10, %r9
	cmpq	(%rsp), %r8
	je	.LBB0_327
.LBB0_165:
	cmpq	$4, %r12
	setb	%r10b
	orb	%al, %r10b
	testb	$1, %r10b
	je	.LBB0_167
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
	jmp	.LBB0_175
.LBB0_167:
	cmpq	$16, %r12
	movq	464(%rsp), %r14
	jae	.LBB0_169
	xorl	%r10d, %r10d
	jmp	.LBB0_173
.LBB0_169:
	xorl	%r10d, %r10d
	.p2align	4
.LBB0_170:
	vmovupd	-96(%rsi,%r10,8), %ymm0
	vmovupd	-64(%rsi,%r10,8), %ymm1
	vmovupd	-32(%rsi,%r10,8), %ymm2
	vmovupd	(%rsi,%r10,8), %ymm3
	vmulpd	(%r14,%r10,8), %ymm0, %ymm0
	vmulpd	32(%r14,%r10,8), %ymm1, %ymm1
	vmulpd	64(%r14,%r10,8), %ymm2, %ymm2
	vmulpd	96(%r14,%r10,8), %ymm3, %ymm3
	vmovupd	%ymm0, -96(%rdi,%r10,8)
	vmovupd	%ymm1, -64(%rdi,%r10,8)
	vmovupd	%ymm2, -32(%rdi,%r10,8)
	vmovupd	%ymm3, (%rdi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rdx
	jne	.LBB0_170
	cmpq	%rdx, %r12
	je	.LBB0_164
	movq	%rdx, %r10
	movq	%rdx, %r11
	testb	$12, %r12b
	je	.LBB0_175
	.p2align	4
.LBB0_173:
	vmovupd	(%r15,%r10,8), %ymm0
	vmulpd	(%r14,%r10,8), %ymm0, %ymm0
	vmovupd	%ymm0, (%r9,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rcx
	jne	.LBB0_173
	movq	%rcx, %r11
	cmpq	%rcx, %r12
	je	.LBB0_164
.LBB0_175:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_178
	movq	%r11, %r10
	.p2align	4
.LBB0_177:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_177
.LBB0_178:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_164
	.p2align	4
.LBB0_179:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	vmovsd	8(%r15,%r10,8), %xmm0
	vmulsd	8(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r9,%r10,8)
	vmovsd	16(%r15,%r10,8), %xmm0
	vmulsd	16(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r9,%r10,8)
	vmovsd	24(%r15,%r10,8), %xmm0
	vmulsd	24(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r9,%r10,8)
	vmovsd	32(%r15,%r10,8), %xmm0
	vmulsd	32(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r9,%r10,8)
	vmovsd	40(%r15,%r10,8), %xmm0
	vmulsd	40(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r9,%r10,8)
	vmovsd	48(%r15,%r10,8), %xmm0
	vmulsd	48(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r9,%r10,8)
	vmovsd	56(%r15,%r10,8), %xmm0
	vmulsd	56(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r9,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_179
	jmp	.LBB0_164
.LBB0_180:
	cmpq	$1, %rdi
	jbe	.LBB0_273
	movq	%rbx, %rcx
	subq	%r15, %rcx
	movq	%rbx, %rdx
	subq	%rbp, %rdx
	movq	%r11, %rsi
	andq	%rax, %rsi
	addq	$12, %rax
	andq	%r11, %rax
	leaq	96(%rbx), %rdi
	xorl	%r8d, %r8d
	movq	%rbx, %r9
	movq	32(%rsp), %r12
	jmp	.LBB0_183
.LBB0_182:
	incq	%r8
	movq	8(%rsp), %r10
	addq	%r10, %rdi
	addq	%r10, %r9
	cmpq	(%rsp), %r8
	je	.LBB0_327
.LBB0_183:
	cmpq	$4, %r12
	jae	.LBB0_190
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
.LBB0_185:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_188
	movq	%r11, %r10
	.p2align	4
.LBB0_187:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_187
.LBB0_188:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_182
	.p2align	4
.LBB0_189:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	vmovsd	8(%r15,%r10,8), %xmm0
	vmulsd	8(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r9,%r10,8)
	vmovsd	16(%r15,%r10,8), %xmm0
	vmulsd	16(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r9,%r10,8)
	vmovsd	24(%r15,%r10,8), %xmm0
	vmulsd	24(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r9,%r10,8)
	vmovsd	32(%r15,%r10,8), %xmm0
	vmulsd	32(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r9,%r10,8)
	vmovsd	40(%r15,%r10,8), %xmm0
	vmulsd	40(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r9,%r10,8)
	vmovsd	48(%r15,%r10,8), %xmm0
	vmulsd	48(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r9,%r10,8)
	vmovsd	56(%r15,%r10,8), %xmm0
	vmulsd	56(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r9,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_189
	jmp	.LBB0_182
.LBB0_190:
	movq	8(%rsp), %r10
	imulq	%r8, %r10
	leaq	(%rcx,%r10), %r11
	cmpq	$128, %r11
	movq	464(%rsp), %r14
	jb	.LBB0_198
	addq	%rdx, %r10
	movl	$0, %r11d
	cmpq	$128, %r10
	jb	.LBB0_185
	xorl	%r10d, %r10d
	cmpq	$16, %r12
	jb	.LBB0_196
	.p2align	4
.LBB0_193:
	vmovupd	(%r15,%r10,8), %ymm0
	vmovupd	32(%r15,%r10,8), %ymm1
	vmovupd	64(%r15,%r10,8), %ymm2
	vmovupd	96(%r15,%r10,8), %ymm3
	vmulpd	(%r14,%r10,8), %ymm0, %ymm0
	vmulpd	32(%r14,%r10,8), %ymm1, %ymm1
	vmulpd	64(%r14,%r10,8), %ymm2, %ymm2
	vmulpd	96(%r14,%r10,8), %ymm3, %ymm3
	vmovupd	%ymm0, -96(%rdi,%r10,8)
	vmovupd	%ymm1, -64(%rdi,%r10,8)
	vmovupd	%ymm2, -32(%rdi,%r10,8)
	vmovupd	%ymm3, (%rdi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rsi
	jne	.LBB0_193
	cmpq	%rsi, %r12
	je	.LBB0_182
	movq	%rsi, %r10
	movq	%rsi, %r11
	testb	$12, %r12b
	je	.LBB0_185
	.p2align	4
.LBB0_196:
	vmovupd	(%r15,%r10,8), %ymm0
	vmulpd	(%r14,%r10,8), %ymm0, %ymm0
	vmovupd	%ymm0, (%r9,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rax
	jne	.LBB0_196
	movq	%rax, %r11
	cmpq	%rax, %r12
	je	.LBB0_182
	jmp	.LBB0_185
.LBB0_198:
	xorl	%r11d, %r11d
	jmp	.LBB0_185
.LBB0_199:
	movabsq	$2305843009213693951, %rax
	cmpq	$1, %rdi
	jbe	.LBB0_291
	addq	(%rsp), %rax
	movq	16(%rsp), %r10
	imulq	%r10, %rax
	leaq	8(%r15,%rax,8), %rax
	leaq	(%r14,%r9,8), %rcx
	cmpq	%rax, %r13
	setb	%al
	movq	24(%rsp), %rsi
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	cmpq	%rcx, %r13
	setb	%al
	cmpq	%rsi, %r14
	setb	%cl
	andb	%al, %cl
	cmpq	$0, 8(%rsp)
	sets	%al
	orb	%cl, %al
	orb	%dl, %al
	movabsq	$9223372036854775792, %rcx
	movq	%r9, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r9, %rcx
	leaq	96(%r13), %rsi
	xorl	%edi, %edi
	movq	%r13, %r8
	movq	%r10, %r13
	movq	32(%rsp), %r12
	jmp	.LBB0_202
.LBB0_201:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_202:
	cmpq	$4, %r12
	setb	%r10b
	movq	%rdi, %r9
	imulq	%r13, %r9
	orb	%al, %r10b
	testb	$1, %r10b
	je	.LBB0_204
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
	jmp	.LBB0_213
.LBB0_204:
	cmpq	$16, %r12
	movq	464(%rsp), %r14
	jae	.LBB0_206
	xorl	%r10d, %r10d
	jmp	.LBB0_210
.LBB0_206:
	vbroadcastsd	(%r15,%r9,8), %ymm0
	xorl	%r10d, %r10d
	.p2align	4
.LBB0_207:
	vmulpd	(%r14,%r10,8), %ymm0, %ymm1
	vmulpd	32(%r14,%r10,8), %ymm0, %ymm2
	vmulpd	64(%r14,%r10,8), %ymm0, %ymm3
	vmulpd	96(%r14,%r10,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rsi,%r10,8)
	vmovupd	%ymm2, -64(%rsi,%r10,8)
	vmovupd	%ymm3, -32(%rsi,%r10,8)
	vmovupd	%ymm4, (%rsi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rdx
	jne	.LBB0_207
	cmpq	%rdx, %r12
	je	.LBB0_201
	movq	%rdx, %r10
	movq	%rdx, %r11
	testb	$12, %r12b
	je	.LBB0_213
.LBB0_210:
	vbroadcastsd	(%r15,%r9,8), %ymm0
	.p2align	4
.LBB0_211:
	vmulpd	(%r14,%r10,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%r8,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rcx
	jne	.LBB0_211
	movq	%rcx, %r11
	cmpq	%rcx, %r12
	je	.LBB0_201
.LBB0_213:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_216
	movq	%r11, %r10
	.p2align	4
.LBB0_215:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_215
.LBB0_216:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_201
	.p2align	4
.LBB0_217:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	8(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	16(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	24(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	32(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	40(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	48(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	56(%r14,%r10,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_217
	jmp	.LBB0_201
.LBB0_218:
	cmpq	$1, %rdi
	jbe	.LBB0_309
	leaq	(%rbp,%r11,8), %rcx
	cmpq	%rax, %rbx
	setb	%al
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	cmpq	%rcx, %rbx
	setb	%al
	cmpq	%rsi, %rbp
	setb	%cl
	andb	%al, %cl
	cmpq	$0, 8(%rsp)
	sets	%al
	orb	%cl, %al
	orb	%dl, %al
	movabsq	$9223372036854775792, %rcx
	movq	%r11, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r11, %rcx
	leaq	96(%rbx), %rsi
	xorl	%edi, %edi
	movq	%rbx, %r8
	movq	32(%rsp), %r14
	jmp	.LBB0_221
.LBB0_220:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_221:
	cmpq	$4, %r14
	setb	%r9b
	orb	%al, %r9b
	testb	$1, %r9b
	je	.LBB0_223
	xorl	%r10d, %r10d
	movq	464(%rsp), %rbx
	jmp	.LBB0_232
.LBB0_223:
	cmpq	$16, %r14
	movq	464(%rsp), %rbx
	jae	.LBB0_225
	xorl	%r9d, %r9d
	jmp	.LBB0_229
.LBB0_225:
	vbroadcastsd	(%r15), %ymm0
	xorl	%r9d, %r9d
	.p2align	4
.LBB0_226:
	vmulpd	(%rbx,%r9,8), %ymm0, %ymm1
	vmulpd	32(%rbx,%r9,8), %ymm0, %ymm2
	vmulpd	64(%rbx,%r9,8), %ymm0, %ymm3
	vmulpd	96(%rbx,%r9,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rsi,%r9,8)
	vmovupd	%ymm2, -64(%rsi,%r9,8)
	vmovupd	%ymm3, -32(%rsi,%r9,8)
	vmovupd	%ymm4, (%rsi,%r9,8)
	addq	$16, %r9
	cmpq	%r9, %rdx
	jne	.LBB0_226
	cmpq	%rdx, %r14
	je	.LBB0_220
	movq	%rdx, %r9
	movq	%rdx, %r10
	testb	$12, %r14b
	je	.LBB0_232
.LBB0_229:
	vbroadcastsd	(%r15), %ymm0
	.p2align	4
.LBB0_230:
	vmulpd	(%rbx,%r9,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%r8,%r9,8)
	addq	$4, %r9
	cmpq	%r9, %rcx
	jne	.LBB0_230
	movq	%rcx, %r10
	cmpq	%rcx, %r14
	je	.LBB0_220
.LBB0_232:
	movl	%r14d, %r11d
	subl	%r10d, %r11d
	movq	%r10, %r9
	andl	$7, %r11d
	je	.LBB0_235
	movq	%r10, %r9
	.p2align	4
.LBB0_234:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	incq	%r9
	decq	%r11
	jne	.LBB0_234
.LBB0_235:
	subq	%r14, %r10
	cmpq	$-8, %r10
	ja	.LBB0_220
	.p2align	4
.LBB0_236:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	8(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	16(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	24(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	32(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	40(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	48(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	56(%rbx,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r9,8)
	addq	$8, %r9
	cmpq	%r9, %r14
	jne	.LBB0_236
	jmp	.LBB0_220
.LBB0_237:
	leaq	8(%rbp,%rdx,8), %rdx
	cmpq	%rsi, %rbx
	setb	%sil
	cmpq	%rcx, %r15
	setb	%dil
	andb	%sil, %dil
	cmpq	%rdx, %rbx
	setb	%dl
	cmpq	%rcx, %rbp
	setb	%sil
	andb	%dl, %sil
	cmpq	$0, 8(%rsp)
	sets	%cl
	orb	%sil, %cl
	orb	%dil, %cl
	movq	%r11, %rdx
	andq	%rax, %rdx
	addq	$12, %rax
	andq	%r11, %rax
	leaq	96(%rbx), %rsi
	xorl	%edi, %edi
	movq	%rbx, %r8
	movq	32(%rsp), %r12
	jmp	.LBB0_239
.LBB0_238:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_239:
	cmpq	$4, %r12
	setb	%r10b
	movq	%rdi, %r9
	imulq	480(%rsp), %r9
	orb	%cl, %r10b
	testb	$1, %r10b
	je	.LBB0_241
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
	jmp	.LBB0_250
.LBB0_241:
	cmpq	$16, %r12
	movq	464(%rsp), %r14
	jae	.LBB0_243
	xorl	%r10d, %r10d
	jmp	.LBB0_247
.LBB0_243:
	vbroadcastsd	(%r14,%r9,8), %ymm0
	xorl	%r10d, %r10d
	.p2align	4
.LBB0_244:
	vmulpd	(%r15,%r10,8), %ymm0, %ymm1
	vmulpd	32(%r15,%r10,8), %ymm0, %ymm2
	vmulpd	64(%r15,%r10,8), %ymm0, %ymm3
	vmulpd	96(%r15,%r10,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rsi,%r10,8)
	vmovupd	%ymm2, -64(%rsi,%r10,8)
	vmovupd	%ymm3, -32(%rsi,%r10,8)
	vmovupd	%ymm4, (%rsi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rdx
	jne	.LBB0_244
	cmpq	%rdx, %r12
	je	.LBB0_238
	movq	%rdx, %r10
	movq	%rdx, %r11
	testb	$12, %r12b
	je	.LBB0_250
.LBB0_247:
	vbroadcastsd	(%r14,%r9,8), %ymm0
	.p2align	4
.LBB0_248:
	vmulpd	(%r15,%r10,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%r8,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rax
	jne	.LBB0_248
	movq	%rax, %r11
	cmpq	%rax, %r12
	je	.LBB0_238
.LBB0_250:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_253
	movq	%r11, %r10
	.p2align	4
.LBB0_252:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_252
.LBB0_253:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_238
	.p2align	4
.LBB0_254:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	vmovsd	8(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r10,8)
	vmovsd	16(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r10,8)
	vmovsd	24(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r10,8)
	vmovsd	32(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r10,8)
	vmovsd	40(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r10,8)
	vmovsd	48(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r10,8)
	vmovsd	56(%r15,%r10,8), %xmm0
	vmulsd	(%r14,%r9,8), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_254
	jmp	.LBB0_238
.LBB0_255:
	addq	(%rsp), %rcx
	movq	16(%rsp), %r10
	imulq	%r10, %rcx
	addq	%r9, %rcx
	leaq	(%r15,%rcx,8), %rcx
	cmpq	%rcx, %r13
	setb	%cl
	movq	24(%rsp), %rsi
	cmpq	%rsi, %r15
	setb	%dl
	andb	%cl, %dl
	movq	%r10, %rcx
	orq	%r9, %rcx
	testq	%rax, %rcx
	setne	%cl
	leaq	8(%r14), %rax
	orb	%dl, %cl
	cmpq	%rax, %r13
	setb	%dl
	cmpq	%rsi, %r14
	setb	%al
	andb	%dl, %al
	orb	%cl, %al
	movabsq	$8070450532247928816, %rcx
	movq	%r9, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r9, %rcx
	leaq	96(%r15), %rsi
	shlq	$3, %r10
	leaq	96(%r13), %rdi
	xorl	%r8d, %r8d
	movq	%r13, %r9
	movq	%r10, %r13
	movq	32(%rsp), %r12
	jmp	.LBB0_257
.LBB0_256:
	incq	%r8
	addq	%r13, %rsi
	movq	8(%rsp), %r10
	addq	%r10, %rdi
	addq	%r13, %r15
	addq	%r10, %r9
	cmpq	(%rsp), %r8
	je	.LBB0_327
.LBB0_257:
	cmpq	$4, %r12
	setb	%r10b
	orb	%al, %r10b
	testb	$1, %r10b
	je	.LBB0_259
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
	jmp	.LBB0_268
.LBB0_259:
	cmpq	$16, %r12
	movq	464(%rsp), %r14
	jae	.LBB0_261
	xorl	%r10d, %r10d
	jmp	.LBB0_265
.LBB0_261:
	vbroadcastsd	(%r14), %ymm0
	xorl	%r10d, %r10d
	.p2align	4
.LBB0_262:
	vmulpd	-96(%rsi,%r10,8), %ymm0, %ymm1
	vmulpd	-64(%rsi,%r10,8), %ymm0, %ymm2
	vmulpd	-32(%rsi,%r10,8), %ymm0, %ymm3
	vmulpd	(%rsi,%r10,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rdi,%r10,8)
	vmovupd	%ymm2, -64(%rdi,%r10,8)
	vmovupd	%ymm3, -32(%rdi,%r10,8)
	vmovupd	%ymm4, (%rdi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rdx
	jne	.LBB0_262
	cmpq	%rdx, %r12
	je	.LBB0_256
	movq	%rdx, %r10
	movq	%rdx, %r11
	testb	$12, %r12b
	je	.LBB0_268
.LBB0_265:
	vbroadcastsd	(%r14), %ymm0
	.p2align	4
.LBB0_266:
	vmulpd	(%r15,%r10,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%r9,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rcx
	jne	.LBB0_266
	movq	%rcx, %r11
	cmpq	%rcx, %r12
	je	.LBB0_256
.LBB0_268:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_271
	movq	%r11, %r10
	.p2align	4
.LBB0_270:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_270
.LBB0_271:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_256
	.p2align	4
.LBB0_272:
	vmovsd	(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, (%r9,%r10,8)
	vmovsd	8(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r9,%r10,8)
	vmovsd	16(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r9,%r10,8)
	vmovsd	24(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r9,%r10,8)
	vmovsd	32(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r9,%r10,8)
	vmovsd	40(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r9,%r10,8)
	vmovsd	48(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r9,%r10,8)
	vmovsd	56(%r15,%r10,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r9,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_272
	jmp	.LBB0_256
.LBB0_273:
	movq	112(%rsp), %rcx
	leaq	(%rbx,%rcx,8), %rcx
	leaq	(%r15,%r11,8), %rdx
	leaq	8(%rbp), %rsi
	cmpq	%rdx, %rbx
	setb	%dl
	cmpq	%rcx, %r15
	setb	%dil
	andb	%dl, %dil
	cmpq	%rsi, %rbx
	setb	%dl
	cmpq	%rcx, %rbp
	setb	%sil
	andb	%dl, %sil
	cmpq	$0, 8(%rsp)
	sets	%cl
	orb	%sil, %cl
	orb	%dil, %cl
	movq	%r11, %rdx
	andq	%rax, %rdx
	addq	$12, %rax
	andq	%r11, %rax
	leaq	96(%rbx), %rsi
	xorl	%edi, %edi
	movq	%rbx, %r8
	movq	32(%rsp), %r14
	jmp	.LBB0_275
.LBB0_274:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_275:
	cmpq	$4, %r14
	setb	%r9b
	orb	%cl, %r9b
	testb	$1, %r9b
	je	.LBB0_277
	xorl	%r10d, %r10d
	movq	464(%rsp), %rbx
	jmp	.LBB0_286
.LBB0_277:
	cmpq	$16, %r14
	movq	464(%rsp), %rbx
	jae	.LBB0_279
	xorl	%r9d, %r9d
	jmp	.LBB0_283
.LBB0_279:
	vbroadcastsd	(%rbx), %ymm0
	xorl	%r9d, %r9d
	.p2align	4
.LBB0_280:
	vmulpd	(%r15,%r9,8), %ymm0, %ymm1
	vmulpd	32(%r15,%r9,8), %ymm0, %ymm2
	vmulpd	64(%r15,%r9,8), %ymm0, %ymm3
	vmulpd	96(%r15,%r9,8), %ymm0, %ymm4
	vmovupd	%ymm1, -96(%rsi,%r9,8)
	vmovupd	%ymm2, -64(%rsi,%r9,8)
	vmovupd	%ymm3, -32(%rsi,%r9,8)
	vmovupd	%ymm4, (%rsi,%r9,8)
	addq	$16, %r9
	cmpq	%r9, %rdx
	jne	.LBB0_280
	cmpq	%rdx, %r14
	je	.LBB0_274
	movq	%rdx, %r9
	movq	%rdx, %r10
	testb	$12, %r14b
	je	.LBB0_286
.LBB0_283:
	vbroadcastsd	(%rbx), %ymm0
	.p2align	4
.LBB0_284:
	vmulpd	(%r15,%r9,8), %ymm0, %ymm1
	vmovupd	%ymm1, (%r8,%r9,8)
	addq	$4, %r9
	cmpq	%r9, %rax
	jne	.LBB0_284
	movq	%rax, %r10
	cmpq	%rax, %r14
	je	.LBB0_274
.LBB0_286:
	movl	%r14d, %r11d
	subl	%r10d, %r11d
	movq	%r10, %r9
	andl	$7, %r11d
	je	.LBB0_289
	movq	%r10, %r9
	.p2align	4
.LBB0_288:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	incq	%r9
	decq	%r11
	jne	.LBB0_288
.LBB0_289:
	subq	%r14, %r10
	cmpq	$-8, %r10
	ja	.LBB0_274
	.p2align	4
.LBB0_290:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	vmovsd	8(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r9,8)
	vmovsd	16(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r9,8)
	vmovsd	24(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r9,8)
	vmovsd	32(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r9,8)
	vmovsd	40(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r9,8)
	vmovsd	48(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r9,8)
	vmovsd	56(%r15,%r9,8), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r9,8)
	addq	$8, %r9
	cmpq	%r9, %r14
	jne	.LBB0_290
	jmp	.LBB0_274
.LBB0_291:
	addq	(%rsp), %rax
	movq	16(%rsp), %r10
	imulq	%r10, %rax
	leaq	8(%r15,%rax,8), %rax
	leaq	8(%r14), %rcx
	cmpq	%rax, %r13
	setb	%al
	movq	24(%rsp), %rsi
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	cmpq	%rcx, %r13
	setb	%al
	cmpq	%rsi, %r14
	setb	%cl
	andb	%al, %cl
	movq	%r9, %rax
	shrq	$60, %rax
	andl	$1, %eax
	orb	%cl, %al
	orb	%dl, %al
	movabsq	$8070450532247928816, %rcx
	movq	%r9, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r9, %rcx
	leaq	96(%r13), %rsi
	xorl	%edi, %edi
	movq	%r13, %r8
	movq	%r10, %r13
	movq	32(%rsp), %r12
	jmp	.LBB0_293
.LBB0_292:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_293:
	cmpq	$4, %r12
	setb	%r10b
	movq	%rdi, %r9
	imulq	%r13, %r9
	orb	%al, %r10b
	testb	$1, %r10b
	je	.LBB0_295
	xorl	%r11d, %r11d
	movq	464(%rsp), %r14
	jmp	.LBB0_304
.LBB0_295:
	cmpq	$16, %r12
	movq	464(%rsp), %r14
	jae	.LBB0_297
	xorl	%r10d, %r10d
	jmp	.LBB0_301
.LBB0_297:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	xorl	%r10d, %r10d
	.p2align	4
.LBB0_298:
	vmovupd	%ymm0, -96(%rsi,%r10,8)
	vmovupd	%ymm0, -64(%rsi,%r10,8)
	vmovupd	%ymm0, -32(%rsi,%r10,8)
	vmovupd	%ymm0, (%rsi,%r10,8)
	addq	$16, %r10
	cmpq	%r10, %rdx
	jne	.LBB0_298
	cmpq	%rdx, %r12
	je	.LBB0_292
	movq	%rdx, %r10
	movq	%rdx, %r11
	testb	$12, %r12b
	je	.LBB0_304
.LBB0_301:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	.p2align	4
.LBB0_302:
	vmovupd	%ymm0, (%r8,%r10,8)
	addq	$4, %r10
	cmpq	%r10, %rcx
	jne	.LBB0_302
	movq	%rcx, %r11
	cmpq	%rcx, %r12
	je	.LBB0_292
.LBB0_304:
	movl	%r12d, %ebx
	subl	%r11d, %ebx
	movq	%r11, %r10
	andl	$7, %ebx
	je	.LBB0_307
	movq	%r11, %r10
	.p2align	4
.LBB0_306:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	incq	%r10
	decq	%rbx
	jne	.LBB0_306
.LBB0_307:
	subq	%r12, %r11
	cmpq	$-8, %r11
	ja	.LBB0_292
	.p2align	4
.LBB0_308:
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r10,8)
	vmovsd	(%r15,%r9,8), %xmm0
	vmulsd	(%r14), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r10,8)
	addq	$8, %r10
	cmpq	%r10, %r12
	jne	.LBB0_308
	jmp	.LBB0_292
.LBB0_309:
	leaq	8(%rbp), %rcx
	cmpq	%rax, %rbx
	setb	%al
	cmpq	%rsi, %r15
	setb	%dl
	andb	%al, %dl
	cmpq	%rcx, %rbx
	setb	%al
	cmpq	%rsi, %rbp
	setb	%cl
	andb	%al, %cl
	movq	%r11, %rax
	shrq	$60, %rax
	andl	$1, %eax
	orb	%cl, %al
	orb	%dl, %al
	movabsq	$8070450532247928816, %rcx
	movq	%r11, %rdx
	andq	%rcx, %rdx
	orq	$12, %rcx
	andq	%r11, %rcx
	leaq	96(%rbx), %rsi
	xorl	%edi, %edi
	movq	%rbx, %r8
	movq	32(%rsp), %r14
	jmp	.LBB0_311
.LBB0_310:
	incq	%rdi
	movq	8(%rsp), %r9
	addq	%r9, %rsi
	addq	%r9, %r8
	cmpq	(%rsp), %rdi
	je	.LBB0_327
.LBB0_311:
	cmpq	$4, %r14
	setb	%r9b
	orb	%al, %r9b
	testb	$1, %r9b
	je	.LBB0_313
	xorl	%r10d, %r10d
	movq	464(%rsp), %rbx
	jmp	.LBB0_322
.LBB0_313:
	cmpq	$16, %r14
	movq	464(%rsp), %rbx
	jae	.LBB0_315
	xorl	%r9d, %r9d
	jmp	.LBB0_319
.LBB0_315:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	xorl	%r9d, %r9d
	.p2align	4
.LBB0_316:
	vmovupd	%ymm0, -96(%rsi,%r9,8)
	vmovupd	%ymm0, -64(%rsi,%r9,8)
	vmovupd	%ymm0, -32(%rsi,%r9,8)
	vmovupd	%ymm0, (%rsi,%r9,8)
	addq	$16, %r9
	cmpq	%r9, %rdx
	jne	.LBB0_316
	cmpq	%rdx, %r14
	je	.LBB0_310
	movq	%rdx, %r9
	movq	%rdx, %r10
	testb	$12, %r14b
	je	.LBB0_322
.LBB0_319:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vbroadcastsd	%xmm0, %ymm0
	.p2align	4
.LBB0_320:
	vmovupd	%ymm0, (%r8,%r9,8)
	addq	$4, %r9
	cmpq	%r9, %rcx
	jne	.LBB0_320
	movq	%rcx, %r10
	cmpq	%rcx, %r14
	je	.LBB0_310
.LBB0_322:
	movl	%r14d, %r11d
	subl	%r10d, %r11d
	movq	%r10, %r9
	andl	$7, %r11d
	je	.LBB0_325
	movq	%r10, %r9
	.p2align	4
.LBB0_324:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	incq	%r9
	decq	%r11
	jne	.LBB0_324
.LBB0_325:
	subq	%r14, %r10
	cmpq	$-8, %r10
	ja	.LBB0_310
	.p2align	4
.LBB0_326:
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, (%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 8(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 16(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 24(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 32(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 40(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 48(%r8,%r9,8)
	vmovsd	(%r15), %xmm0
	vmulsd	(%rbx), %xmm0, %xmm0
	vmovsd	%xmm0, 56(%r8,%r9,8)
	addq	$8, %r9
	cmpq	%r9, %r14
	jne	.LBB0_326
	jmp	.LBB0_310
.LBB0_327:
	movq	$0, 168(%rsp)
	movq	216(%rsp), %r13
	movq	%r13, %rdi
	movabsq	$NRT_incref, %rbx
	vzeroupper
	callq	*%rbx
	movq	256(%rsp), %r14
	movq	%r14, %rdi
	callq	*%rbx
	vxorpd	%xmm0, %xmm0, %xmm0
	vmovupd	%ymm0, 368(%rsp)
	vmovupd	%ymm0, 336(%rsp)
	movq	$0, 400(%rsp)
	movabsq	$_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE, %rax
	xorl	%r15d, %r15d
	leaq	336(%rsp), %rdi
	leaq	168(%rsp), %rsi
	movl	$8, %r9d
	movq	%r13, %rdx
	movq	112(%rsp), %r8
	xorl	%ecx, %ecx
	pushq	496(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	496(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	176(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	496(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	496(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	272(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	288(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	304(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	%r14
	.cfi_adjust_cfa_offset 8
	pushq	80(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	$8
	.cfi_adjust_cfa_offset 8
	pushq	88(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	128(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	184(%rsp)
	.cfi_adjust_cfa_offset 8
	vzeroupper
	callq	*%rax
	addq	$112, %rsp
	.cfi_adjust_cfa_offset -112
	testl	%eax, %eax
	je	.LBB0_329
	movq	168(%rsp), %rbx
	movq	152(%rsp), %rdi
	movabsq	$NRT_decref, %rax
	callq	*%rax
	movq	176(%rsp), %rax
	movq	%rbx, (%rax)
	jmp	.LBB0_29
.LBB0_329:
	vmovups	336(%rsp), %ymm0
	vmovups	%ymm0, 32(%rsp)
	vmovups	368(%rsp), %ymm0
	vmovups	%ymm0, 176(%rsp)
	movq	400(%rsp), %rbx
	movq	%r14, %rdi
	movabsq	$NRT_decref, %r12
	vzeroupper
	callq	*%r12
	movq	%r13, %rdi
	callq	*%r12
	movq	152(%rsp), %rdi
	callq	*%r12
	movq	224(%rsp), %rax
	vmovups	32(%rsp), %ymm0
	vmovups	%ymm0, (%rax)
	vmovupd	176(%rsp), %ymm0
	vmovupd	%ymm0, 32(%rax)
	movq	%rbx, 64(%rax)
	movq	%r14, %rdi
	vzeroupper
	callq	*%r12
	movq	%r13, %rdi
	callq	*%r12
	jmp	.LBB0_30
.LBB0_330:
	movabsq	$.const.picklebuf.139798920073600, %rax
	jmp	.LBB0_28
.LBB0_331:
	movabsq	$.const.picklebuf.139798927748736, %rax
	jmp	.LBB0_28
.Lfunc_end0:
	.size	_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end0-_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	_ZN7cpython8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN7cpython8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN7cpython8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	movabsq	$".const.main.<locals>.nb_blas_fused", %rsi
	movabsq	$PyArg_UnpackTuple, %r10
	xorl	%ebx, %ebx
	leaq	200(%rsp), %r8
	leaq	192(%rsp), %r9
	movl	$2, %edx
	movl	$2, %ecx
	xorl	%eax, %eax
	callq	*%r10
	movq	$0, 128(%rsp)
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 208(%rsp)
	vmovups	%ymm0, 240(%rsp)
	movq	$0, 272(%rsp)
	testl	%eax, %eax
	je	.LBB1_23
	movabsq	$_ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
	movq	(%rax), %r14
	testq	%r14, %r14
	je	.LBB1_2
	movq	200(%rsp), %rdi
	vmovups	%ymm0, 368(%rsp)
	vmovups	%ymm0, 400(%rsp)
	movq	$0, 432(%rsp)
	movabsq	$NRT_adapt_ndarray_from_python, %r12
	leaq	368(%rsp), %rsi
	vzeroupper
	callq	*%r12
	cmpq	$8, 392(%rsp)
	setne	%cl
	testl	%eax, %eax
	setne	%bl
	orb	%cl, %bl
	cmpb	$1, %bl
	je	.LBB1_5
	testb	%bl, %bl
	jne	.LBB1_22
.LBB1_7:
	movq	%r14, 184(%rsp)
	movq	368(%rsp), %rax
	movq	%rax, 104(%rsp)
	movq	376(%rsp), %rax
	movq	%rax, 120(%rsp)
	movq	384(%rsp), %rax
	movq	%rax, 112(%rsp)
	movq	400(%rsp), %r13
	movq	408(%rsp), %rbp
	movq	416(%rsp), %r14
	movq	424(%rsp), %r15
	movq	432(%rsp), %rbx
	movq	192(%rsp), %rdi
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 448(%rsp)
	vmovups	%ymm0, 472(%rsp)
	leaq	448(%rsp), %rsi
	vzeroupper
	callq	*%r12
	testl	%eax, %eax
	jne	.LBB1_9
	cmpq	$8, 472(%rsp)
	jne	.LBB1_9
	movq	448(%rsp), %r12
	vmovups	456(%rsp), %xmm0
	vmovaps	480(%rsp), %xmm1
	movq	496(%rsp), %rax
	vxorps	%xmm2, %xmm2, %xmm2
	vmovups	%ymm2, 288(%rsp)
	vmovups	%ymm2, 320(%rsp)
	movq	$0, 352(%rsp)
	movq	%rax, 88(%rsp)
	vmovups	%xmm1, 72(%rsp)
	vmovups	%xmm0, 48(%rsp)
	movq	%r12, 40(%rsp)
	movq	%rbx, 32(%rsp)
	movq	%r15, 24(%rsp)
	movq	%r14, 16(%rsp)
	movq	%rbp, 8(%rsp)
	movq	%r13, (%rsp)
	movq	$8, 64(%rsp)
	movabsq	$_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
	leaq	288(%rsp), %rdi
	leaq	128(%rsp), %rsi
	movl	$8, %r9d
	movq	104(%rsp), %rbx
	movq	%rbx, %rdx
	movq	120(%rsp), %rcx
	movq	112(%rsp), %r8
	vzeroupper
	callq	*%rax
	movl	%eax, %r13d
	movq	128(%rsp), %r15
	movq	288(%rsp), %rax
	movq	%rax, 144(%rsp)
	movq	296(%rsp), %rax
	movq	%rax, 152(%rsp)
	movq	304(%rsp), %rax
	movq	%rax, 136(%rsp)
	movq	312(%rsp), %rax
	movq	%rax, 120(%rsp)
	movq	320(%rsp), %rax
	movq	%rax, 112(%rsp)
	movq	328(%rsp), %rax
	movq	%rax, 176(%rsp)
	movq	336(%rsp), %rax
	movq	%rax, 168(%rsp)
	movq	344(%rsp), %rax
	movq	%rax, 160(%rsp)
	movq	352(%rsp), %r14
	movabsq	$NRT_decref, %rbp
	movq	%rbx, %rdi
	callq	*%rbp
	movq	%r12, %rdi
	callq	*%rbp
	testl	%r13d, %r13d
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
	movq	%r14, 104(%rsp)
	movq	136(%rsp), %r13
	movq	144(%rsp), %r14
	movq	152(%rsp), %r15
	movq	184(%rsp), %rax
	movq	24(%rax), %rdi
	testq	%rdi, %rdi
	je	.LBB1_13
	movabsq	$PyList_GetItem, %rax
	xorl	%esi, %esi
	callq	*%rax
	movq	%rax, %rbx
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
	xorl	%ebx, %ebx
	jmp	.LBB1_23
.LBB1_13:
	movabsq	$PyExc_RuntimeError, %rdi
	movabsq	$".const.`env.consts` is NULL in `read_const`", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	xorl	%ebx, %ebx
.LBB1_14:
	movabsq	$.const.pickledata.139799574043104, %rdi
	movabsq	$.const.pickledata.139799574043104.sha1, %rdx
	movabsq	$numba_unpickle, %rax
	movl	$32, %esi
	callq	*%rax
	movq	%r14, 208(%rsp)
	movq	%r15, 216(%rsp)
	movq	%r13, 224(%rsp)
	movq	120(%rsp), %rcx
	movq	%rcx, 232(%rsp)
	movq	112(%rsp), %rcx
	movq	%rcx, 240(%rsp)
	movq	176(%rsp), %rcx
	movq	%rcx, 248(%rsp)
	movq	168(%rsp), %rcx
	movq	%rcx, 256(%rsp)
	movq	160(%rsp), %rcx
	movq	%rcx, 264(%rsp)
	movq	104(%rsp), %rcx
	movq	%rcx, 272(%rsp)
	movabsq	$NRT_adapt_ndarray_to_python_acqref, %r9
	leaq	208(%rsp), %rdi
	movq	%rax, %rsi
	movl	$2, %edx
	movl	$1, %ecx
	movq	%rbx, %r8
	callq	*%r9
	movq	%rax, %rbx
	movq	%r14, %rdi
	callq	*%rbp
.LBB1_23:
	movq	%rbx, %rax
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
	movabsq	$".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", %rsi
	jmp	.LBB1_3
.LBB1_5:
	movabsq	$PyExc_TypeError, %rdi
	movabsq	$".const.can't unbox array from PyObject into native value.  The object maybe of a different type", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	testb	%bl, %bl
	je	.LBB1_7
	jmp	.LBB1_22
.LBB1_9:
	movabsq	$PyExc_TypeError, %rdi
	movabsq	$".const.can't unbox array from PyObject into native value.  The object maybe of a different type", %rsi
	movabsq	$PyErr_SetString, %rax
	callq	*%rax
	movabsq	$NRT_decref, %rax
	movq	104(%rsp), %rdi
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
	.size	_ZN7cpython8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end1-_ZN7cpython8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	cfunc._ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	cfunc._ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
cfunc._ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	movq	%r8, %rax
	movq	%rcx, %r8
	movq	%rdx, %rcx
	movq	%rsi, %rdx
	movq	%rdi, %rbx
	vmovups	288(%rsp), %ymm0
	vmovups	320(%rsp), %ymm1
	vmovaps	352(%rsp), %xmm2
	movq	368(%rsp), %rsi
	vxorps	%xmm3, %xmm3, %xmm3
	vmovups	%ymm3, 192(%rsp)
	vmovups	%ymm3, 160(%rsp)
	movq	$0, 224(%rsp)
	movq	$0, 104(%rsp)
	movq	%rsi, 88(%rsp)
	vmovups	%xmm2, 72(%rsp)
	vmovups	%ymm1, 40(%rsp)
	vmovups	%ymm0, 8(%rsp)
	movq	%r9, (%rsp)
	movabsq	$_ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %r10
	leaq	160(%rsp), %rdi
	leaq	104(%rsp), %rsi
	movq	%rax, %r9
	vzeroupper
	callq	*%r10
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
	je	.LBB2_7
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
	jle	.LBB2_4
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
	je	.LBB2_6
.LBB2_9:
	movabsq	$numba_do_raise, %rax
	movq	%r15, %rdi
	callq	*%rax
.LBB2_6:
	movabsq	$".const.<numba.core.cpu.CPUContext object at 0x7f2578f08790>", %rdi
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
.LBB2_7:
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
.LBB2_4:
	.cfi_def_cfa_offset 288
	movq	16(%r14), %rdx
	movabsq	$numba_unpickle, %rax
	callq	*%rax
	movq	%rax, %r15
	testq	%r15, %r15
	jne	.LBB2_9
	jmp	.LBB2_6
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
	jmp	.LBB2_7
.Lfunc_end2:
	.size	cfunc._ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end2-cfunc._ZN8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
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

	.weak	_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE
	.p2align	4
	.type	_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@function
_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE:
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
	subq	$120, %rsp
	.cfi_def_cfa_offset 176
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%r9, 40(%rsp)
	movq	%r8, 32(%rsp)
	movq	%rcx, 24(%rsp)
	movq	%rdx, %r15
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movq	216(%rsp), %rbp
	movq	184(%rsp), %r12
	movq	$0, 16(%rsp)
	movabsq	$NRT_incref, %r13
	movq	%rdx, %rdi
	callq	*%r13
	movq	%rbp, %rdi
	callq	*%r13
	cmpq	$0, 192(%rsp)
	je	.LBB4_1
	movq	%rbx, 8(%rsp)
	movabsq	$.const.picklebuf.139798921938304, %rax
	testq	%r12, %r12
	js	.LBB4_15
	cmpq	$0, 264(%rsp)
	js	.LBB4_15
	movq	%r12, %rbp
	imulq	264(%rsp), %rbp
	movabsq	$.const.picklebuf.139798921939328, %rax
	jo	.LBB4_15
	movabsq	$-1152921504606846976, %rcx
	addq	%rbp, %rcx
	movabsq	$-2305843009213693952, %rdx
	cmpq	%rdx, %rcx
	jb	.LBB4_15
	leaq	(,%rbp,8), %rdi
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	movl	$32, %esi
	callq	*%rax
	testq	%rax, %rax
	je	.LBB4_14
	movq	%rax, %r13
	movq	280(%rsp), %r10
	movq	176(%rsp), %rbx
	movq	264(%rsp), %r12
	leaq	(,%r12,8), %r11
	movq	24(%rax), %rax
	vxorps	%xmm0, %xmm0, %xmm0
	vmovups	%ymm0, 80(%rsp)
	vmovups	%ymm0, 48(%rsp)
	movq	$0, 112(%rsp)
	subq	$8, %rsp
	.cfi_adjust_cfa_offset 8
	leaq	56(%rsp), %rdi
	leaq	24(%rsp), %rsi
	movq	%r15, %rdx
	movq	32(%rsp), %rcx
	movq	40(%rsp), %r8
	movq	48(%rsp), %r9
	pushq	$8
	.cfi_adjust_cfa_offset 8
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	pushq	%r12
	.cfi_adjust_cfa_offset 8
	movq	216(%rsp), %r11
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	pushq	%rax
	.cfi_adjust_cfa_offset 8
	pushq	$8
	.cfi_adjust_cfa_offset 8
	pushq	%rbp
	.cfi_adjust_cfa_offset 8
	pushq	$0
	.cfi_adjust_cfa_offset 8
	pushq	%r13
	.cfi_adjust_cfa_offset 8
	pushq	%r10
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	%r12
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	movq	360(%rsp), %r12
	pushq	%r12
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	360(%rsp)
	.cfi_adjust_cfa_offset 8
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	pushq	%rbx
	.cfi_adjust_cfa_offset 8
	movabsq	$_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE, %rax
	vzeroupper
	callq	*%rax
	addq	$192, %rsp
	.cfi_adjust_cfa_offset -192
	testl	%eax, %eax
	je	.LBB4_17
	movq	16(%rsp), %rax
.LBB4_15:
	movq	8(%rsp), %rcx
	movq	%rax, (%rcx)
	movl	$1, %eax
	jmp	.LBB4_18
.LBB4_1:
	movq	%rbx, %r13
	movabsq	$NRT_decref, %rbx
	movq	%rbp, %rdi
	callq	*%rbx
	movq	%r15, %rdi
	callq	*%rbx
	movabsq	$.const.picklebuf.139798920047424, %rax
	testq	%r12, %r12
	js	.LBB4_2
	cmpq	$0, 264(%rsp)
	movq	%r13, %rbp
	js	.LBB4_8
	movq	%r12, %r13
	imulq	264(%rsp), %r13
	movabsq	$.const.picklebuf.139798920051072, %rax
	jo	.LBB4_8
	movabsq	$-1152921504606846976, %rcx
	addq	%r13, %rcx
	movabsq	$-2305843009213693952, %rdx
	cmpq	%rdx, %rcx
	jb	.LBB4_8
	leaq	(,%r13,8), %rbx
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	movq	%rbx, %rdi
	movl	$32, %esi
	callq	*%rax
	testq	%rax, %rax
	je	.LBB4_7
	movq	%rax, %r15
	movq	264(%rsp), %rax
	leaq	(,%rax,8), %rbp
	movq	24(%r15), %r12
	movabsq	$memset, %rax
	movq	%r12, %rdi
	xorl	%esi, %esi
	movq	%rbx, %rdx
	callq	*%rax
	xorl	%eax, %eax
	movq	%r15, (%r14)
	movq	$0, 8(%r14)
	movq	%r13, 16(%r14)
	movq	$8, 24(%r14)
	movq	%r12, 32(%r14)
	movq	184(%rsp), %rcx
	movq	%rcx, 40(%r14)
	movq	264(%rsp), %rcx
	movq	%rcx, 48(%r14)
	movq	%rbp, 56(%r14)
	movq	$8, 64(%r14)
	jmp	.LBB4_18
.LBB4_17:
	vmovups	48(%rsp), %ymm0
	vmovups	80(%rsp), %ymm1
	movq	112(%rsp), %rax
	vmovups	%ymm0, (%r14)
	vmovups	%ymm1, 32(%r14)
	movq	%rax, 64(%r14)
	movabsq	$NRT_decref, %rbx
	movq	%r13, %rdi
	vzeroupper
	callq	*%rbx
	movq	%r12, %rdi
	callq	*%rbx
	movq	%r15, %rdi
	callq	*%rbx
	xorl	%eax, %eax
.LBB4_18:
	addq	$120, %rsp
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
.LBB4_14:
	.cfi_def_cfa_offset 176
	movabsq	$.const.picklebuf.139798927748736.9, %rax
	jmp	.LBB4_15
.LBB4_2:
	movq	%r13, %rbp
	jmp	.LBB4_8
.LBB4_7:
	movabsq	$.const.picklebuf.139798927748736.17, %rax
.LBB4_8:
	movq	%rax, (%rbp)
	movl	$1, %eax
	jmp	.LBB4_18
.Lfunc_end4:
	.size	_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE, .Lfunc_end4-_ZN5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE
	.cfi_endproc

	.weak	NRT_decref
	.p2align	4
	.type	NRT_decref,@function
NRT_decref:
	.cfi_startproc
	testq	%rdi, %rdi
	je	.LBB5_2
	#MEMBARRIER
	lock		decq	(%rdi)
	je	.LBB5_3
.LBB5_2:
	retq
.LBB5_3:
	#MEMBARRIER
	movabsq	$NRT_MemInfo_call_dtor, %rax
	jmpq	*%rax
.Lfunc_end5:
	.size	NRT_decref, .Lfunc_end5-NRT_decref
	.cfi_endproc

	.weak	_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE
	.p2align	4
	.type	_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@function
_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE:
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
	subq	$72, %rsp
	.cfi_def_cfa_offset 128
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rdx, %rbx
	movq	%rsi, %rbp
	movq	%rdi, 64(%rsp)
	movq	240(%rsp), %r15
	movq	168(%rsp), %r12
	movq	144(%rsp), %r13
	movl	$0, 12(%rsp)
	movq	$0, 56(%rsp)
	movq	$0, 48(%rsp)
	movl	$0, 8(%rsp)
	movq	$0, 40(%rsp)
	movq	$0, 32(%rsp)
	movl	$0, 4(%rsp)
	movq	$0, 24(%rsp)
	movq	$0, 16(%rsp)
	movl	$0, (%rsp)
	movabsq	$NRT_incref, %r14
	movq	%rdx, %rdi
	callq	*%r14
	movq	%r12, %rdi
	movq	%r15, %r12
	callq	*%r14
	movq	%r15, %rdi
	callq	*%r14
	cmpq	208(%rsp), %r13
	jne	.LBB6_1
	movq	288(%rsp), %r15
	movq	280(%rsp), %r14
	movq	136(%rsp), %rax
	xorq	%r14, %rax
	movq	216(%rsp), %rcx
	xorq	%r15, %rcx
	orq	%rax, %rcx
	je	.LBB6_5
	movabsq	$.const.picklebuf.139798919596864, %rax
	jmp	.LBB6_4
.LBB6_1:
	movabsq	$.const.picklebuf.139798921939136, %rax
	jmp	.LBB6_4
.LBB6_5:
	cmpq	$2147483647, %r14
	jg	.LBB6_6
	cmpq	$2147483647, %r13
	jg	.LBB6_6
	cmpq	$2147483647, %r15
	jle	.LBB6_9
.LBB6_6:
	movabsq	$.const.picklebuf.139798919642624, %rax
.LBB6_4:
	movq	%rax, (%rbp)
	movl	$1, %eax
.LBB6_14:
	addq	$72, %rsp
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
.LBB6_9:
	.cfi_def_cfa_offset 128
	movq	272(%rsp), %r11
	movq	264(%rsp), %rbp
	testq	%r13, %r13
	je	.LBB6_12
	testq	%r14, %r14
	je	.LBB6_12
	testq	%r15, %r15
	je	.LBB6_12
	movq	200(%rsp), %rax
	movq	128(%rsp), %r10
	cmpq	$1, %r15
	jne	.LBB6_16
	cmpq	$1, %r14
	jne	.LBB6_20
	movabsq	$numba_xxdot, %rbp
	movl	$100, %edi
	xorl	%esi, %esi
	movq	%r13, %rdx
	movq	%r10, %rcx
	movq	%rax, %r8
	movq	%r11, %r13
	movq	%r11, %r9
	callq	*%rbp
	testl	%eax, %eax
	movq	264(%rsp), %rbp
	je	.LBB6_13
	movabsq	$numba_gil_ensure, %rax
	leaq	12(%rsp), %rdi
	callq	*%rax
	movabsq	$".const.BLAS wrapper returned with an error", %rdi
	movabsq	$Py_FatalError, %rax
	callq	*%rax
.LBB6_16:
	cmpq	$1, %r14
	movq	%r14, %rbp
	movabsq	$4607182418800017408, %rcx
	jne	.LBB6_25
	movq	%rcx, 40(%rsp)
	movq	$0, 32(%rsp)
	leaq	32(%rsp), %r14
	leaq	40(%rsp), %r8
	movl	$100, %edi
	movl	$110, %esi
	movq	%r15, %rdx
	movq	%r13, %rcx
	movq	%rax, %r9
	movq	%r11, %r13
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	pushq	%r14
	.cfi_adjust_cfa_offset 8
	pushq	%r10
	.cfi_adjust_cfa_offset 8
	pushq	%r15
	.cfi_adjust_cfa_offset 8
	movabsq	$numba_xxgemv, %rax
	callq	*%rax
	addq	$32, %rsp
	.cfi_adjust_cfa_offset -32
	testl	%eax, %eax
	movq	%rbp, %r14
	movq	264(%rsp), %rbp
	je	.LBB6_13
	movabsq	$numba_gil_ensure, %rax
	leaq	4(%rsp), %rdi
	callq	*%rax
	movabsq	$".const.BLAS wrapper returned with an error", %rdi
	movabsq	$Py_FatalError, %rax
	callq	*%rax
.LBB6_20:
	movabsq	$4607182418800017408, %rcx
	movq	%rcx, 56(%rsp)
	movq	$0, 48(%rsp)
	movq	%r14, %rbp
	movabsq	$numba_xxgemv, %r14
	leaq	56(%rsp), %r8
	movl	$100, %edi
	movl	$110, %esi
	movq	%rbp, %rdx
	movq	%r13, %rcx
	movq	%r10, %r9
	movq	%r11, %r13
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	leaq	56(%rsp), %r10
	pushq	%r10
	.cfi_adjust_cfa_offset 8
	pushq	%rax
	.cfi_adjust_cfa_offset 8
	pushq	%rbp
	.cfi_adjust_cfa_offset 8
	callq	*%r14
	movq	%rbp, %r14
	addq	$32, %rsp
	.cfi_adjust_cfa_offset -32
	testl	%eax, %eax
	movq	264(%rsp), %rbp
	je	.LBB6_13
	movabsq	$numba_gil_ensure, %rax
	leaq	8(%rsp), %rdi
	callq	*%rax
	movabsq	$".const.BLAS wrapper returned with an error", %rdi
	movabsq	$Py_FatalError, %rax
	callq	*%rax
.LBB6_25:
	movq	%rcx, 24(%rsp)
	movq	$0, 16(%rsp)
	leaq	16(%rsp), %r14
	movl	$100, %edi
	movl	$110, %esi
	movl	$116, %edx
	movq	%r15, %rcx
	movq	%rbp, %r8
	movq	%r13, %r9
	pushq	%r15
	.cfi_adjust_cfa_offset 8
	movq	%r11, %r13
	pushq	%r11
	.cfi_adjust_cfa_offset 8
	pushq	%r14
	.cfi_adjust_cfa_offset 8
	pushq	%rbp
	.cfi_adjust_cfa_offset 8
	pushq	%r10
	.cfi_adjust_cfa_offset 8
	pushq	%r15
	.cfi_adjust_cfa_offset 8
	pushq	%rax
	.cfi_adjust_cfa_offset 8
	leaq	80(%rsp), %rax
	pushq	%rax
	.cfi_adjust_cfa_offset 8
	movabsq	$numba_xxgemm, %rax
	callq	*%rax
	addq	$64, %rsp
	.cfi_adjust_cfa_offset -64
	testl	%eax, %eax
	movq	%rbp, %r14
	movq	264(%rsp), %rbp
	jne	.LBB6_26
.LBB6_13:
	movq	304(%rsp), %rax
	movq	296(%rsp), %rcx
	movq	248(%rsp), %rdx
	movq	64(%rsp), %rsi
	movq	%r12, (%rsi)
	movq	%rdx, 8(%rsi)
	movq	256(%rsp), %rdx
	movq	%rdx, 16(%rsi)
	movq	%rbp, 24(%rsi)
	movq	%r13, 32(%rsi)
	movq	%r14, 40(%rsi)
	movq	%r15, 48(%rsi)
	movq	%rcx, 56(%rsi)
	movq	%rax, 64(%rsi)
	movabsq	$NRT_decref, %r14
	movq	168(%rsp), %rdi
	callq	*%r14
	movq	%rbx, %rdi
	callq	*%r14
	xorl	%eax, %eax
	jmp	.LBB6_14
.LBB6_12:
	movq	%rbp, %rdx
	imulq	256(%rsp), %rdx
	movabsq	$memset, %rax
	movq	%r11, %r13
	movq	%r11, %rdi
	xorl	%esi, %esi
	callq	*%rax
	jmp	.LBB6_13
.LBB6_26:
	movabsq	$numba_gil_ensure, %rax
	movq	%rsp, %rdi
	callq	*%rax
	movabsq	$".const.BLAS wrapper returned with an error", %rdi
	movabsq	$Py_FatalError, %rax
	callq	*%rax
.Lfunc_end6:
	.size	_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE, .Lfunc_end6-_ZN5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE
	.cfi_endproc

	.type	.const.pickledata.139798928103424,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.const.pickledata.139798928103424:
	.ascii	"\200\004\225H\000\000\000\000\000\000\000\214\bbuiltins\224\214\023NotImplementedError\224\223\224\214\034incompatible shape for array\224\205\224N\207\224."
	.size	.const.pickledata.139798928103424, 83

	.type	.const.pickledata.139798928103424.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798928103424.sha1:
	.ascii	"\334;\272\203,L7X'=\r\262K\203V\221\257?1l"
	.size	.const.pickledata.139798928103424.sha1, 20

	.type	.const.picklebuf.139798928103424,@object
	.p2align	4, 0x0
.const.picklebuf.139798928103424:
	.quad	.const.pickledata.139798928103424
	.long	83
	.zero	4
	.quad	.const.pickledata.139798928103424.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798928103424, 40

	.type	.const.pickledata.139798919238336,@object
	.p2align	4, 0x0
.const.pickledata.139798919238336:
	.ascii	"\200\004\225\310\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214\245unable to broadcast argument 1 to output array\nFile \"/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/npyimpl.py\", line 372, \224\205\224N\207\224."
	.size	.const.pickledata.139798919238336, 211

	.type	.const.pickledata.139798919238336.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798919238336.sha1:
	.ascii	"\020\017(\005\032\024\315\036M\343=\022\305]\250\272s\342[\301"
	.size	.const.pickledata.139798919238336.sha1, 20

	.type	.const.picklebuf.139798919238336,@object
	.p2align	4, 0x0
.const.picklebuf.139798919238336:
	.quad	.const.pickledata.139798919238336
	.long	211
	.zero	4
	.quad	.const.pickledata.139798919238336.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798919238336, 40

	.type	.const.pickledata.139798920073600,@object
	.p2align	4, 0x0
.const.pickledata.139798920073600:
	.ascii	"\200\004\225~\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214[array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.\224\205\224N\207\224."
	.size	.const.pickledata.139798920073600, 137

	.type	.const.pickledata.139798920073600.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798920073600.sha1:
	.ascii	"X\341N\314\265\007\261\340 i\201t\002#\346\205\313\214<W"
	.size	.const.pickledata.139798920073600.sha1, 20

	.type	.const.picklebuf.139798920073600,@object
	.p2align	4, 0x0
.const.picklebuf.139798920073600:
	.quad	.const.pickledata.139798920073600
	.long	137
	.zero	4
	.quad	.const.pickledata.139798920073600.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798920073600, 40

	.type	".const.main.<locals>.nb_blas_fused",@object
	.p2align	4, 0x0
".const.main.<locals>.nb_blas_fused":
	.asciz	"main.<locals>.nb_blas_fused"
	.size	".const.main.<locals>.nb_blas_fused", 28

	.type	_ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,8,8
	.type	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE",@object
	.p2align	4, 0x0
".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE":
	.asciz	"missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE"
	.size	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e13nb_blas_fusedB2v8B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", 186

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

	.type	".const.<numba.core.cpu.CPUContext object at 0x7f2578f08790>",@object
	.p2align	4, 0x0
".const.<numba.core.cpu.CPUContext object at 0x7f2578f08790>":
	.asciz	"<numba.core.cpu.CPUContext object at 0x7f2578f08790>"
	.size	".const.<numba.core.cpu.CPUContext object at 0x7f2578f08790>", 53

	.type	_ZN08NumbaEnv5numba2np8arrayobj23normalize_reshape_valueB3v17B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEy5ArrayIxLi1E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj23normalize_reshape_valueB3v17B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEy5ArrayIxLi1E1C7mutable7alignedE,8,8
	.type	.const.pickledata.139798921910016,@object
	.p2align	4, 0x0
.const.pickledata.139798921910016:
	.ascii	"\200\004\225\321\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214)total size of new array must be unchanged\224\205\224\214\027normalize_reshape_value\224\214d/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/arrayobj.py\224M\204\b\207\224\207\224."
	.size	.const.pickledata.139798921910016, 220

	.type	.const.pickledata.139798921910016.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798921910016.sha1:
	.ascii	"\327\367-\347\214\330\247\226Yzr\004>\307^'\034\3718\257"
	.size	.const.pickledata.139798921910016.sha1, 20

	.type	.const.picklebuf.139798921910016,@object
	.p2align	4, 0x0
.const.picklebuf.139798921910016:
	.quad	.const.pickledata.139798921910016
	.long	220
	.zero	4
	.quad	.const.pickledata.139798921910016.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798921910016, 40

	.type	.const.pickledata.139798920522816,@object
	.p2align	4, 0x0
.const.pickledata.139798920522816:
	.ascii	"\200\004\225\321\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214)total size of new array must be unchanged\224\205\224\214\027normalize_reshape_value\224\214d/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/arrayobj.py\224M\217\b\207\224\207\224."
	.size	.const.pickledata.139798920522816, 220

	.type	.const.pickledata.139798920522816.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798920522816.sha1:
	.ascii	"\335\351\312;\257c\251\220\3474\000\r\377\020\362KPC\201h"
	.size	.const.pickledata.139798920522816.sha1, 20

	.type	.const.picklebuf.139798920522816,@object
	.p2align	4, 0x0
.const.picklebuf.139798920522816:
	.quad	.const.pickledata.139798920522816
	.long	220
	.zero	4
	.quad	.const.pickledata.139798920522816.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798920522816, 40

	.type	.const.pickledata.139798927836096,@object
	.p2align	4, 0x0
.const.pickledata.139798927836096:
	.ascii	"\200\004\225\306\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214\036multiple negative shape values\224\205\224\214\027normalize_reshape_value\224\214d/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/arrayobj.py\224M\223\b\207\224\207\224."
	.size	.const.pickledata.139798927836096, 209

	.type	.const.pickledata.139798927836096.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798927836096.sha1:
	.ascii	"\2279\374\304\316\003,`\221R)M\302\373\374W\301o\271v"
	.size	.const.pickledata.139798927836096.sha1, 20

	.type	.const.picklebuf.139798927836096,@object
	.p2align	4, 0x0
.const.picklebuf.139798927836096:
	.quad	.const.pickledata.139798927836096
	.long	209
	.zero	4
	.quad	.const.pickledata.139798927836096.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927836096, 40

	.type	_ZN08NumbaEnv13_3cdynamic_3e33__numba_array_expr_0x7f2578e4e2d0B3v18B72c8tJTIeFIjxB2IKSgI4CrvQCk0Z4yRYcWsBAQ4s_2fqEpEUkESQI1_2bmEQRxHRNAA_3d_3dEdd,@object
	.comm	_ZN08NumbaEnv13_3cdynamic_3e33__numba_array_expr_0x7f2578e4e2d0B3v18B72c8tJTIeFIjxB2IKSgI4CrvQCk0Z4yRYcWsBAQ4s_2fqEpEUkESQI1_2bmEQRxHRNAA_3d_3dEdd,8,8
	.type	_ZN08NumbaEnv5numba2np7npyimpl15_broadcast_ontoB3v19B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEx8int64_2ax8int64_2a,@object
	.comm	_ZN08NumbaEnv5numba2np7npyimpl15_broadcast_ontoB3v19B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEx8int64_2ax8int64_2a,8,8
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

	.type	_ZN08NumbaEnv5numba2np6linalg10dot_2_impl12_3clocals_3e12_3clambda_3eB2v9B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np6linalg10dot_2_impl12_3clocals_3e12_3clambda_3eB2v9B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.type	_ZN08NumbaEnv5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np6linalg8dot_2_mm12_3clocals_3e8dot_implB3v10B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_zeros12_3clocals_3e4implB3v11B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_zeros12_3clocals_3e4implB3v11B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB3v12B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB3v12B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,8,8
	.type	.const.pickledata.139798920047424,@object
	.p2align	4, 0x0
.const.pickledata.139798920047424:
	.ascii	"\200\004\225B\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214\037negative dimensions not allowed\224\205\224N\207\224."
	.size	.const.pickledata.139798920047424, 77

	.type	.const.pickledata.139798920047424.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798920047424.sha1:
	.ascii	"3\033\205c\275\271\332\310\0338B\"s\005,Ho\301pk"
	.size	.const.pickledata.139798920047424.sha1, 20

	.type	.const.picklebuf.139798920047424,@object
	.p2align	4, 0x0
.const.picklebuf.139798920047424:
	.quad	.const.pickledata.139798920047424
	.long	77
	.zero	4
	.quad	.const.pickledata.139798920047424.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798920047424, 40

	.type	.const.pickledata.139798920051072,@object
	.p2align	4, 0x0
.const.pickledata.139798920051072:
	.ascii	"\200\004\225~\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214[array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.\224\205\224N\207\224."
	.size	.const.pickledata.139798920051072, 137

	.type	.const.pickledata.139798920051072.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798920051072.sha1:
	.ascii	"X\341N\314\265\007\261\340 i\201t\002#\346\205\313\214<W"
	.size	.const.pickledata.139798920051072.sha1, 20

	.type	.const.picklebuf.139798920051072,@object
	.p2align	4, 0x0
.const.picklebuf.139798920051072:
	.quad	.const.pickledata.139798920051072
	.long	137
	.zero	4
	.quad	.const.pickledata.139798920051072.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798920051072, 40

	.type	.const.pickledata.139798927748736.18,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736.18:
	.ascii	"\200\004\225K\000\000\000\000\000\000\000\214\bbuiltins\224\214\013MemoryError\224\223\224\214'Allocation failed (probably too large).\224\205\224N\207\224."
	.size	.const.pickledata.139798927748736.18, 86

	.type	.const.pickledata.139798927748736.sha1.19,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736.sha1.19:
	.ascii	"\272(\235\201\360\\p \363G|\025sH\004\337e\253\342\t"
	.size	.const.pickledata.139798927748736.sha1.19, 20

	.type	.const.picklebuf.139798927748736.17,@object
	.p2align	4, 0x0
.const.picklebuf.139798927748736.17:
	.quad	.const.pickledata.139798927748736.18
	.long	86
	.zero	4
	.quad	.const.pickledata.139798927748736.sha1.19
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927748736.17, 40

	.type	_ZN08NumbaEnv5numba2np8arrayobj18ol_array_zero_fill12_3clocals_3e4implB2v6B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj18ol_array_zero_fill12_3clocals_3e4implB2v6B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB3v13B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj11ol_np_empty12_3clocals_3e4implB3v13B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE8UniTupleIxLi2EE18dtype_28float64_29,8,8
	.type	.const.pickledata.139798921938304,@object
	.p2align	4, 0x0
.const.pickledata.139798921938304:
	.ascii	"\200\004\225B\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214\037negative dimensions not allowed\224\205\224N\207\224."
	.size	.const.pickledata.139798921938304, 77

	.type	.const.pickledata.139798921938304.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798921938304.sha1:
	.ascii	"3\033\205c\275\271\332\310\0338B\"s\005,Ho\301pk"
	.size	.const.pickledata.139798921938304.sha1, 20

	.type	.const.picklebuf.139798921938304,@object
	.p2align	4, 0x0
.const.picklebuf.139798921938304:
	.quad	.const.pickledata.139798921938304
	.long	77
	.zero	4
	.quad	.const.pickledata.139798921938304.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798921938304, 40

	.type	.const.pickledata.139798921939328,@object
	.p2align	4, 0x0
.const.pickledata.139798921939328:
	.ascii	"\200\004\225~\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214[array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.\224\205\224N\207\224."
	.size	.const.pickledata.139798921939328, 137

	.type	.const.pickledata.139798921939328.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798921939328.sha1:
	.ascii	"X\341N\314\265\007\261\340 i\201t\002#\346\205\313\214<W"
	.size	.const.pickledata.139798921939328.sha1, 20

	.type	.const.picklebuf.139798921939328,@object
	.p2align	4, 0x0
.const.picklebuf.139798921939328:
	.quad	.const.pickledata.139798921939328
	.long	137
	.zero	4
	.quad	.const.pickledata.139798921939328.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798921939328, 40

	.type	_ZN08NumbaEnv5numba2np8arrayobj15_call_allocatorB2v4B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj15_call_allocatorB2v4B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,8,8
	.type	_ZN08NumbaEnv5numba2np8arrayobj18_ol_array_allocate12_3clocals_3e4implB2v5B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,@object
	.comm	_ZN08NumbaEnv5numba2np8arrayobj18_ol_array_allocate12_3clocals_3e4implB2v5B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dEN29typeref_5b_3cclass_20_27numba4core5types8npytypes14Array_27_3e_5dExj,8,8
	.type	.const.pickledata.139798927748736.10,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736.10:
	.ascii	"\200\004\225K\000\000\000\000\000\000\000\214\bbuiltins\224\214\013MemoryError\224\223\224\214'Allocation failed (probably too large).\224\205\224N\207\224."
	.size	.const.pickledata.139798927748736.10, 86

	.type	.const.pickledata.139798927748736.sha1.11,@object
	.p2align	4, 0x0
.const.pickledata.139798927748736.sha1.11:
	.ascii	"\272(\235\201\360\\p \363G|\025sH\004\337e\253\342\t"
	.size	.const.pickledata.139798927748736.sha1.11, 20

	.type	.const.picklebuf.139798927748736.9,@object
	.p2align	4, 0x0
.const.picklebuf.139798927748736.9:
	.quad	.const.pickledata.139798927748736.10
	.long	86
	.zero	4
	.quad	.const.pickledata.139798927748736.sha1.11
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798927748736.9, 40

	.type	_ZN08NumbaEnv5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np6linalg5dot_312_3clocals_3e12_3clambda_3eB3v14B42c8tJTIeFIjxB2IKSgI4CrvQClcaMQ5hEEUSJJgA_3dE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.type	".const.BLAS wrapper returned with an error",@object
	.p2align	4, 0x0
".const.BLAS wrapper returned with an error":
	.asciz	"BLAS wrapper returned with an error"
	.size	".const.BLAS wrapper returned with an error", 36

	.type	_ZN08NumbaEnv5numba2np6linalg8dot_3_mm12_3clocals_3e10check_argsB3v15B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv5numba2np6linalg8dot_3_mm12_3clocals_3e10check_argsB3v15B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAE5ArrayIdLi2E1F7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi2E1C7mutable7alignedE,8,8
	.type	.const.pickledata.139798921939136,@object
	.p2align	4, 0x0
.const.pickledata.139798921939136:
	.ascii	"\200\004\225\324\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214;incompatible array sizes for np.dot(a, b) (matrix * matrix)\224\205\224\214\ncheck_args\224\214b/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/linalg.py\224M\317\002\207\224\207\224."
	.size	.const.pickledata.139798921939136, 223

	.type	.const.pickledata.139798921939136.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798921939136.sha1:
	.ascii	"\031A\364\336\213\272G\005\221_\247W\026n\356\001\377\344<-"
	.size	.const.pickledata.139798921939136.sha1, 20

	.type	.const.picklebuf.139798921939136,@object
	.p2align	4, 0x0
.const.picklebuf.139798921939136:
	.quad	.const.pickledata.139798921939136
	.long	223
	.zero	4
	.quad	.const.pickledata.139798921939136.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798921939136, 40

	.type	.const.pickledata.139798919596864,@object
	.p2align	4, 0x0
.const.pickledata.139798919596864:
	.ascii	"\200\004\225\337\000\000\000\000\000\000\000\214\bbuiltins\224\214\nValueError\224\223\224\214Fincompatible output array size for np.dot(a, b, out) (matrix * matrix)\224\205\224\214\ncheck_args\224\214b/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/linalg.py\224M\322\002\207\224\207\224."
	.size	.const.pickledata.139798919596864, 234

	.type	.const.pickledata.139798919596864.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798919596864.sha1:
	.ascii	"\367\321\025\230\370\274k\356\037\275\335\242s\273D\227\317\313\311}"
	.size	.const.pickledata.139798919596864.sha1, 20

	.type	.const.picklebuf.139798919596864,@object
	.p2align	4, 0x0
.const.picklebuf.139798919596864:
	.quad	.const.pickledata.139798919596864
	.long	234
	.zero	4
	.quad	.const.pickledata.139798919596864.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798919596864, 40

	.type	_ZN08NumbaEnv5numba2np6linalg11check_c_int12_3clocals_3e4implB3v16B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEx,@object
	.comm	_ZN08NumbaEnv5numba2np6linalg11check_c_int12_3clocals_3e4implB3v16B42c8tJTC_2fWQA93W1AaAIYBPIqRBFCjDSZRVAJmaQIAEx,8,8
	.type	.const.pickledata.139798919642624,@object
	.p2align	4, 0x0
.const.pickledata.139798919642624:
	.ascii	"\200\004\225\272\000\000\000\000\000\000\000\214\bbuiltins\224\214\rOverflowError\224\223\224\214$array size too large to fit in C int\224\205\224\214\004impl\224\214b/home/ubuntu/.cache/uv/archive-v0/B6_L5gzg8khCwWRv/lib/python3.11/site-packages/numba/np/linalg.py\224M7\001\207\224\207\224."
	.size	.const.pickledata.139798919642624, 197

	.type	.const.pickledata.139798919642624.sha1,@object
	.p2align	4, 0x0
.const.pickledata.139798919642624.sha1:
	.ascii	"Y\210\333\005\020\004[O\225\232\316\230\016\220\232\306\316\023\r%"
	.size	.const.pickledata.139798919642624.sha1, 20

	.type	.const.picklebuf.139798919642624,@object
	.p2align	4, 0x0
.const.picklebuf.139798919642624:
	.quad	.const.pickledata.139798919642624
	.long	197
	.zero	4
	.quad	.const.pickledata.139798919642624.sha1
	.quad	0
	.long	0
	.zero	4
	.size	.const.picklebuf.139798919642624, 40

	.section	".note.GNU-stack","",@progbits
