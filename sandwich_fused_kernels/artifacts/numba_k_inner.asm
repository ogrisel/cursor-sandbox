	.file	"<string>"
	.section	.rodata.cst32,"aM",@progbits,32
	.p2align	5, 0x0
.LCPI0_0:
	.quad	0
	.quad	1
	.quad	2
	.quad	3
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3, 0x0
.LCPI0_1:
	.quad	4
.LCPI0_2:
	.quad	8
.LCPI0_3:
	.quad	12
.LCPI0_4:
	.quad	16
	.section	.ltext,"axl",@progbits
	.globl	_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	subq	$56, %rsp
	.cfi_def_cfa_offset 112
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rdx, %r15
	movq	%rsi, %r13
	movq	%rdi, %r12
	movq	152(%rsp), %r14
	movq	128(%rsp), %rbp
	movabsq	$NRT_incref, %rbx
	movq	%rdx, %rdi
	callq	*%rbx
	movq	%r14, %rdi
	callq	*%rbx
	testq	%rbp, %rbp
	js	.LBB0_1
	movq	%rbp, %rbx
	imulq	%rbp, %rbx
	movabsq	$.const.picklebuf.139798927689024, %rax
	jo	.LBB0_2
	movabsq	$-1152921504606846976, %rcx
	addq	%rbx, %rcx
	shrq	$61, %rcx
	cmpl	$7, %ecx
	jb	.LBB0_2
	leaq	(,%rbx,8), %r14
	movabsq	$NRT_MemInfo_alloc_aligned, %rax
	movq	%r14, %rdi
	movl	$32, %esi
	callq	*%rax
	testq	%rax, %rax
	je	.LBB0_6
	movq	%rbx, 16(%rsp)
	movq	%r12, 24(%rsp)
	movq	%r15, 32(%rsp)
	leaq	(,%rbp,8), %r12
	movq	%rax, 8(%rsp)
	movq	24(%rax), %rdi
	movabsq	$memset, %rax
	movq	%rdi, (%rsp)
	xorl	%esi, %esi
	movq	%r14, %rdx
	callq	*%rax
	testq	%rbp, %rbp
	je	.LBB0_7
	movq	120(%rsp), %rdx
	testq	%rdx, %rdx
	jle	.LBB0_22
	movq	184(%rsp), %rcx
	movl	%edx, %esi
	andl	$7, %esi
	movabsq	$9223372036854775792, %rdi
	orq	$8, %rdi
	andq	%rdx, %rdi
	movq	%rbp, %r8
	shlq	$6, %r8
	xorl	%r9d, %r9d
	xorl	%r10d, %r10d
	jmp	.LBB0_12
	.p2align	4
.LBB0_21:
	movq	40(%rsp), %r10
	incq	%r10
	addq	$8, %r9
	cmpq	%r10, %rbp
	je	.LBB0_7
.LBB0_12:
	movq	(%rsp), %rax
	movq	%r10, 40(%rsp)
	leaq	(%rax,%r10,8), %rax
	movq	%rax, 48(%rsp)
	xorl	%r14d, %r14d
	xorl	%ebx, %ebx
	jmp	.LBB0_13
	.p2align	4
.LBB0_20:
	leaq	1(%rbx), %rax
	imulq	%rbp, %rbx
	movq	48(%rsp), %rdx
	vmovsd	%xmm0, (%rdx,%rbx,8)
	addq	$8, %r14
	movq	%rax, %rbx
	cmpq	%rbp, %rax
	movq	%r11, %rdx
	je	.LBB0_21
.LBB0_13:
	movq	%rdx, %r11
	vxorpd	%xmm0, %xmm0, %xmm0
	cmpq	$8, %rdx
	jae	.LBB0_15
	xorl	%r15d, %r15d
	jmp	.LBB0_17
	.p2align	4
.LBB0_15:
	movq	112(%rsp), %rdx
	xorl	%r15d, %r15d
	.p2align	4
.LBB0_16:
	leaq	(%rdx,%r14), %rax
	vmovsd	(%rdx,%r14), %xmm1
	vmulsd	(%rcx,%r15,8), %xmm1, %xmm1
	leaq	(%rdx,%r9), %r13
	vmulsd	(%rdx,%r9), %xmm1, %xmm1
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%rax,%rbp,8), %xmm1
	vmulsd	8(%rcx,%r15,8), %xmm1, %xmm1
	leaq	(%rax,%rbp,8), %rax
	leaq	(%r13,%rbp,8), %r10
	vmulsd	(%r13,%rbp,8), %xmm1, %xmm1
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	addq	%r12, %rax
	vmulsd	16(%rcx,%r15,8), %xmm1, %xmm1
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	addq	%r12, %r10
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	vmulsd	24(%rcx,%r15,8), %xmm1, %xmm1
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	addq	%r12, %rax
	addq	%r12, %r10
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	vmulsd	32(%rcx,%r15,8), %xmm1, %xmm1
	addq	%r12, %rax
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	addq	%r12, %r10
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	addq	%r12, %rax
	vmulsd	40(%rcx,%r15,8), %xmm1, %xmm1
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	addq	%r12, %r10
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	vmulsd	48(%rcx,%r15,8), %xmm1, %xmm1
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	addq	%r12, %rax
	addq	%r12, %r10
	vaddsd	%xmm1, %xmm0, %xmm0
	vmovsd	(%r12,%rax), %xmm1
	vmulsd	56(%rcx,%r15,8), %xmm1, %xmm1
	addq	$8, %r15
	vmulsd	(%r12,%r10), %xmm1, %xmm1
	vaddsd	%xmm1, %xmm0, %xmm0
	addq	%r8, %rdx
	cmpq	%r15, %rdi
	jne	.LBB0_16
.LBB0_17:
	testq	%rsi, %rsi
	je	.LBB0_20
	leaq	(%rcx,%r15,8), %rax
	imulq	%r12, %r15
	addq	112(%rsp), %r15
	xorl	%edx, %edx
	.p2align	4
.LBB0_19:
	vmovsd	(%r15,%r14), %xmm1
	vmulsd	(%rax,%rdx,8), %xmm1, %xmm1
	vmulsd	(%r15,%r9), %xmm1, %xmm1
	vaddsd	%xmm1, %xmm0, %xmm0
	incq	%rdx
	addq	%r12, %r15
	cmpq	%rdx, %rsi
	jne	.LBB0_19
	jmp	.LBB0_20
.LBB0_22:
	movabsq	$9223372036854775792, %rax
	movq	%rbp, %rcx
	andq	%rax, %rcx
	vpbroadcastq	%rbp, %ymm0
	orq	$12, %rax
	andq	%rbp, %rax
	movabsq	$9223372036854775804, %rdx
	andq	%rbp, %rdx
	negq	%rdx
	movq	%rbp, %rsi
	negq	%rsi
	xorl	%edi, %edi
	movabsq	$.LCPI0_0, %r8
	vmovdqa	(%r8), %ymm1
	vxorpd	%xmm2, %xmm2, %xmm2
	movabsq	$.LCPI0_1, %r9
	vpbroadcastq	(%r9), %ymm3
	vmovdqa	(%r8), %ymm4
	movabsq	$.LCPI0_2, %r8
	vpbroadcastq	(%r8), %ymm5
	movabsq	$.LCPI0_3, %r8
	vpbroadcastq	(%r8), %ymm6
	movabsq	$.LCPI0_4, %r8
	vpbroadcastq	(%r8), %ymm7
	movq	(%rsp), %r8
	jmp	.LBB0_23
	.p2align	4
.LBB0_36:
	incq	%rdi
	addq	$8, %r8
	cmpq	%rdi, %rbp
	je	.LBB0_7
.LBB0_23:
	cmpq	$4, %rbp
	jae	.LBB0_25
	xorl	%r10d, %r10d
	jmp	.LBB0_34
	.p2align	4
.LBB0_25:
	movq	(%rsp), %r9
	leaq	(%r9,%rdi,8), %r9
	cmpq	$16, %rbp
	jae	.LBB0_27
	xorl	%r11d, %r11d
	jmp	.LBB0_31
	.p2align	4
.LBB0_27:
	movq	%rcx, %r10
	vmovdqa	%ymm4, %ymm8
	.p2align	4
.LBB0_28:
	vpaddq	%ymm3, %ymm8, %ymm9
	vpaddq	%ymm5, %ymm8, %ymm10
	vpaddq	%ymm6, %ymm8, %ymm11
	vxorps	%xmm12, %xmm12, %xmm12
	vpmullq	%ymm0, %ymm8, %ymm12
	vpmullq	%ymm0, %ymm9, %ymm9
	vpmullq	%ymm0, %ymm10, %ymm10
	vpmullq	%ymm0, %ymm11, %ymm11
	kxnorw	%k0, %k0, %k1
	vscatterqpd	%ymm2, (%r9,%ymm12,8) {%k1}
	kxnorw	%k0, %k0, %k1
	vscatterqpd	%ymm2, (%r9,%ymm9,8) {%k1}
	kxnorw	%k0, %k0, %k1
	vscatterqpd	%ymm2, (%r9,%ymm10,8) {%k1}
	kxnorw	%k0, %k0, %k1
	vscatterqpd	%ymm2, (%r9,%ymm11,8) {%k1}
	vpaddq	%ymm7, %ymm8, %ymm8
	addq	$-16, %r10
	jne	.LBB0_28
	cmpq	%rcx, %rbp
	je	.LBB0_36
	movq	%rcx, %r11
	movq	%rcx, %r10
	testb	$12, %bpl
	je	.LBB0_34
.LBB0_31:
	vpbroadcastq	%r11, %ymm8
	vpor	%ymm1, %ymm8, %ymm8
	addq	%rdx, %r11
	.p2align	4
.LBB0_32:
	vxorps	%xmm9, %xmm9, %xmm9
	vpmullq	%ymm0, %ymm8, %ymm9
	kxnorw	%k0, %k0, %k1
	vscatterqpd	%ymm2, (%r9,%ymm9,8) {%k1}
	vpaddq	%ymm3, %ymm8, %ymm8
	addq	$4, %r11
	jne	.LBB0_32
	movq	%rax, %r10
	cmpq	%rax, %rbp
	je	.LBB0_36
.LBB0_34:
	movq	%r12, %r9
	imulq	%r10, %r9
	addq	%r8, %r9
	addq	%rsi, %r10
	.p2align	4
.LBB0_35:
	movq	$0, (%r9)
	addq	%r12, %r9
	incq	%r10
	jne	.LBB0_35
	jmp	.LBB0_36
.LBB0_7:
	movq	24(%rsp), %rax
	movq	8(%rsp), %rcx
	movq	%rcx, (%rax)
	movq	$0, 8(%rax)
	movq	16(%rsp), %rcx
	movq	%rcx, 16(%rax)
	movq	$8, 24(%rax)
	movq	(%rsp), %rcx
	movq	%rcx, 32(%rax)
	movq	%rbp, 40(%rax)
	movq	%rbp, 48(%rax)
	movq	%r12, 56(%rax)
	movq	$8, 64(%rax)
	movabsq	$NRT_decref, %rbx
	movq	152(%rsp), %rdi
	vzeroupper
	callq	*%rbx
	movq	32(%rsp), %rdi
	callq	*%rbx
	xorl	%eax, %eax
.LBB0_8:
	addq	$56, %rsp
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
.LBB0_1:
	.cfi_def_cfa_offset 112
	movabsq	$.const.picklebuf.139798927552384, %rax
	jmp	.LBB0_2
.LBB0_6:
	movabsq	$.const.picklebuf.139798927748736, %rax
.LBB0_2:
	movq	%rax, (%r13)
	movl	$1, %eax
	jmp	.LBB0_8
.Lfunc_end0:
	.size	_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end0-_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	_ZN7cpython8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	_ZN7cpython8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
_ZN7cpython8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	movabsq	$".const.main.<locals>.nb_k_inner", %rsi
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
	movabsq	$_ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
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
	movabsq	$_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
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
	movabsq	$".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", %rsi
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
	.size	_ZN7cpython8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end1-_ZN7cpython8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.cfi_endproc

	.globl	cfunc._ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
	.p2align	4
	.type	cfunc._ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@function
cfunc._ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE:
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
	movabsq	$_ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, %rax
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
	movabsq	$".const.<numba.core.cpu.CPUContext object at 0x7f25796e6cd0>", %rdi
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
	.size	cfunc._ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE, .Lfunc_end2-cfunc._ZN8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE
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

	.type	".const.main.<locals>.nb_k_inner",@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
".const.main.<locals>.nb_k_inner":
	.asciz	"main.<locals>.nb_k_inner"
	.size	".const.main.<locals>.nb_k_inner", 25

	.type	_ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,@object
	.comm	_ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE,8,8
	.type	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE",@object
	.p2align	4, 0x0
".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE":
	.asciz	"missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE"
	.size	".const.missing Environment: _ZN08NumbaEnv8__main__4main12_3clocals_3e10nb_k_innerB2v1B38c8tJTIeFIjxB2IKSgI4CrvQClQZ6FczSBAA_3dE5ArrayIdLi2E1C7mutable7alignedE5ArrayIdLi1E1C7mutable7alignedE", 183

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

	.type	".const.<numba.core.cpu.CPUContext object at 0x7f25796e6cd0>",@object
	.p2align	4, 0x0
".const.<numba.core.cpu.CPUContext object at 0x7f25796e6cd0>":
	.asciz	"<numba.core.cpu.CPUContext object at 0x7f25796e6cd0>"
	.size	".const.<numba.core.cpu.CPUContext object at 0x7f25796e6cd0>", 53

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
