0000000000ad2c00 <dgemm_kernel_HASWELL>:
  ad2c00:	48 83 ec 60          	sub    rsp,0x60
  ad2c04:	48 89 1c 24          	mov    QWORD PTR [rsp],rbx
  ad2c08:	48 89 6c 24 08       	mov    QWORD PTR [rsp+0x8],rbp
  ad2c0d:	4c 89 64 24 10       	mov    QWORD PTR [rsp+0x10],r12
  ad2c12:	4c 89 6c 24 18       	mov    QWORD PTR [rsp+0x18],r13
  ad2c17:	4c 89 74 24 20       	mov    QWORD PTR [rsp+0x20],r14
  ad2c1c:	4c 89 7c 24 28       	mov    QWORD PTR [rsp+0x28],r15
  ad2c21:	c5 f8 77             	vzeroupper
  ad2c24:	4c 8b 54 24 68       	mov    r10,QWORD PTR [rsp+0x68]
  ad2c29:	48 89 e3             	mov    rbx,rsp
  ad2c2c:	48 81 ec 80 70 00 00 	sub    rsp,0x7080
  ad2c33:	48 81 e4 00 f0 ff ff 	and    rsp,0xfffffffffffff000
  ad2c3a:	48 83 ff 00          	cmp    rdi,0x0
  ad2c3e:	0f 84 40 6d 00 00    	je     ad9984 <dgemm_kernel_HASWELL+0x6d84>
  ad2c44:	48 83 fe 00          	cmp    rsi,0x0
  ad2c48:	0f 84 36 6d 00 00    	je     ad9984 <dgemm_kernel_HASWELL+0x6d84>
  ad2c4e:	48 83 fa 00          	cmp    rdx,0x0
  ad2c52:	0f 84 2c 6d 00 00    	je     ad9984 <dgemm_kernel_HASWELL+0x6d84>
  ad2c58:	49 89 fd             	mov    r13,rdi
  ad2c5b:	48 89 74 24 28       	mov    QWORD PTR [rsp+0x28],rsi
  ad2c60:	49 89 d4             	mov    r12,rdx
  ad2c63:	c5 fb 11 44 24 30    	vmovsd QWORD PTR [rsp+0x30],xmm0
  ad2c69:	49 c1 e2 03          	shl    r10,0x3
  ad2c6d:	48 8b 44 24 28       	mov    rax,QWORD PTR [rsp+0x28]
  ad2c72:	48 31 d2             	xor    rdx,rdx
  ad2c75:	48 c7 c7 18 00 00 00 	mov    rdi,0x18
  ad2c7c:	48 f7 f7             	div    rdi
  ad2c7f:	48 89 44 24 18       	mov    QWORD PTR [rsp+0x18],rax
  ad2c84:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
  ad2c89:	4c 8b 74 24 18       	mov    r14,QWORD PTR [rsp+0x18]
  ad2c8e:	49 83 fe 00          	cmp    r14,0x0
  ad2c92:	0f 84 11 3f 00 00    	je     ad6ba9 <dgemm_kernel_HASWELL+0x3fa9>
  ad2c98:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  ad2c9f:	00 
  ad2ca0:	4c 89 e0             	mov    rax,r12
  ad2ca3:	48 c1 e0 03          	shl    rax,0x3
  ad2ca7:	4c 89 c7             	mov    rdi,r8
  ad2caa:	4d 8d 3c c0          	lea    r15,[r8+rax*8]
  ad2cae:	4d 89 f8             	mov    r8,r15
  ad2cb1:	48 8d b4 24 80 00 00 	lea    rsi,[rsp+0x80]
  ad2cb8:	00 
  ad2cb9:	4c 89 e0             	mov    rax,r12
  ad2cbc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  ad2cc0:	c5 fc 10 0f          	vmovups ymm1,YMMWORD PTR [rdi]
  ad2cc4:	c5 fc 10 57 20       	vmovups ymm2,YMMWORD PTR [rdi+0x20]
  ad2cc9:	c4 c1 7c 10 1f       	vmovups ymm3,YMMWORD PTR [r15]
  ad2cce:	c5 fc 11 0e          	vmovups YMMWORD PTR [rsi],ymm1
  ad2cd2:	c5 fc 11 56 20       	vmovups YMMWORD PTR [rsi+0x20],ymm2
  ad2cd7:	c5 fc 11 5e 40       	vmovups YMMWORD PTR [rsi+0x40],ymm3
  ad2cdc:	48 83 c7 40          	add    rdi,0x40
  ad2ce0:	49 83 c7 40          	add    r15,0x40
  ad2ce4:	48 83 c6 60          	add    rsi,0x60
  ad2ce8:	48 ff c8             	dec    rax
  ad2ceb:	75 d3                	jne    ad2cc0 <dgemm_kernel_HASWELL+0xc0>
  ad2ced:	4d 89 cf             	mov    r15,r9
  ad2cf0:	4f 8d 0c d1          	lea    r9,[r9+r10*8]
  ad2cf4:	4f 8d 0c 91          	lea    r9,[r9+r10*4]
  ad2cf8:	48 89 cf             	mov    rdi,rcx
  ad2cfb:	48 81 c7 80 00 00 00 	add    rdi,0x80
  ad2d02:	4d 89 eb             	mov    r11,r13
  ad2d05:	49 c1 fb 02          	sar    r11,0x2
  ad2d09:	0f 84 9f 12 00 00    	je     ad3fae <dgemm_kernel_HASWELL+0x13ae>
  ad2d0f:	90                   	nop
  ad2d10:	48 8d b4 24 80 00 00 	lea    rsi,[rsp+0x80]
  ad2d17:	00 
  ad2d18:	48 83 c6 60          	add    rsi,0x60
  ad2d1c:	4c 89 e0             	mov    rax,r12
  ad2d1f:	48 c1 f8 03          	sar    rax,0x3
  ad2d23:	48 83 f8 02          	cmp    rax,0x2
  ad2d27:	0f 8c f9 0b 00 00    	jl     ad3926 <dgemm_kernel_HASWELL+0xd26>
  ad2d2d:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad2d34:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad2d39:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad2d40:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad2d46:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad2d4d:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad2d52:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad2d59:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad2d5e:	c5 f5 59 e0          	vmulpd ymm4,ymm1,ymm0
  ad2d62:	0f 18 8e 60 01 00 00 	prefetcht0 BYTE PTR [rsi+0x160]
  ad2d69:	c5 6d 59 c0          	vmulpd ymm8,ymm2,ymm0
  ad2d6d:	c5 65 59 e0          	vmulpd ymm12,ymm3,ymm0
  ad2d71:	0f 18 8e a0 01 00 00 	prefetcht0 BYTE PTR [rsi+0x1a0]
  ad2d78:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad2d7e:	c5 f5 59 e8          	vmulpd ymm5,ymm1,ymm0
  ad2d82:	c5 6d 59 c8          	vmulpd ymm9,ymm2,ymm0
  ad2d86:	c5 65 59 e8          	vmulpd ymm13,ymm3,ymm0
  ad2d8a:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad2d90:	c5 f5 59 f0          	vmulpd ymm6,ymm1,ymm0
  ad2d94:	c5 6d 59 d0          	vmulpd ymm10,ymm2,ymm0
  ad2d98:	48 83 c6 60          	add    rsi,0x60
  ad2d9c:	c5 65 59 f0          	vmulpd ymm14,ymm3,ymm0
  ad2da0:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad2da6:	c5 f5 59 f8          	vmulpd ymm7,ymm1,ymm0
  ad2daa:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad2daf:	c5 6d 59 d8          	vmulpd ymm11,ymm2,ymm0
  ad2db3:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad2db8:	c5 65 59 f8          	vmulpd ymm15,ymm3,ymm0
  ad2dbc:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad2dc1:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad2dc7:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad2dcc:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad2dd1:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad2dd6:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad2ddc:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad2de1:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad2de6:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad2deb:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad2df1:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad2df6:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad2dfb:	48 83 c7 40          	add    rdi,0x40
  ad2dff:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad2e04:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad2e0b:	ff ff 
  ad2e0d:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad2e12:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad2e16:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad2e1b:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad2e20:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad2e25:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad2e2a:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad2e31:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad2e38:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad2e3e:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad2e45:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad2e4a:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad2e51:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad2e56:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad2e5d:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad2e62:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad2e68:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad2e6d:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad2e72:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad2e77:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad2e7d:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad2e82:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad2e87:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad2e8c:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad2e92:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad2e97:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad2e9c:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad2ea1:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad2ea6:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad2eab:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad2eb0:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad2eb6:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad2ebb:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad2ec0:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad2ec5:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad2ecb:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad2ed0:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad2ed5:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad2eda:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad2ee0:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad2ee5:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad2eea:	48 83 c7 40          	add    rdi,0x40
  ad2eee:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad2ef3:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad2efa:	ff ff 
  ad2efc:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad2f01:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad2f05:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad2f0a:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad2f0f:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad2f14:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad2f19:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad2f20:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad2f27:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad2f2d:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad2f34:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad2f39:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad2f40:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad2f45:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad2f4c:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad2f51:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad2f57:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad2f5c:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad2f61:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad2f66:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad2f6c:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad2f71:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad2f76:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad2f7b:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad2f81:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad2f86:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad2f8b:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad2f90:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad2f95:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad2f9a:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad2f9f:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad2fa5:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad2faa:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad2faf:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad2fb4:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad2fba:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad2fbf:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad2fc4:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad2fc9:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad2fcf:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad2fd4:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad2fd9:	48 83 c7 40          	add    rdi,0x40
  ad2fdd:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad2fe2:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad2fe9:	ff ff 
  ad2feb:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad2ff0:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad2ff4:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad2ff9:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad2ffe:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3003:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3008:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad300f:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3016:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad301c:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3023:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3028:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad302f:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3034:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad303b:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3040:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3046:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad304b:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3050:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3055:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad305b:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3060:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3065:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad306a:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3070:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3075:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad307a:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad307f:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3084:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3089:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad308e:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3094:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3099:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad309e:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad30a3:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad30a9:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad30ae:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad30b3:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad30b8:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad30be:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad30c3:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad30c8:	48 83 c7 40          	add    rdi,0x40
  ad30cc:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad30d1:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad30d8:	ff ff 
  ad30da:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad30df:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad30e3:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad30e8:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad30ed:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad30f2:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad30f7:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad30fe:	48 83 e8 02          	sub    rax,0x2
  ad3102:	0f 84 dd 03 00 00    	je     ad34e5 <dgemm_kernel_HASWELL+0x8e5>
  ad3108:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  ad310f:	00 00 00 
  ad3112:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  ad3119:	00 00 00 
  ad311c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  ad3120:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3127:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad312d:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3134:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3139:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3140:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3145:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad314c:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3151:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3157:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad315c:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3161:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3166:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad316c:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3171:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3176:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad317b:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3181:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3186:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad318b:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3190:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3195:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad319a:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad319f:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad31a5:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad31aa:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad31af:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad31b4:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad31ba:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad31bf:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad31c4:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad31c9:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad31cf:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad31d4:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad31d9:	48 83 c7 40          	add    rdi,0x40
  ad31dd:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad31e2:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad31e9:	ff ff 
  ad31eb:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad31f0:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad31f4:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad31f9:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad31fe:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3203:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3208:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad320f:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3216:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad321c:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3223:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3228:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad322f:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3234:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad323b:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3240:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3246:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad324b:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3250:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3255:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad325b:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3260:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3265:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad326a:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3270:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3275:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad327a:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad327f:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3284:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3289:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad328e:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3294:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3299:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad329e:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad32a3:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad32a9:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad32ae:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad32b3:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad32b8:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad32be:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad32c3:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad32c8:	48 83 c7 40          	add    rdi,0x40
  ad32cc:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad32d1:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad32d8:	ff ff 
  ad32da:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad32df:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad32e3:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad32e8:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad32ed:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad32f2:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad32f7:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad32fe:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3305:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad330b:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3312:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3317:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad331e:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3323:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad332a:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad332f:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3335:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad333a:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad333f:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3344:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad334a:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad334f:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3354:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3359:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad335f:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3364:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3369:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad336e:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3373:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3378:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad337d:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3383:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3388:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad338d:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3392:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad3398:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad339d:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad33a2:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad33a7:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad33ad:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad33b2:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad33b7:	48 83 c7 40          	add    rdi,0x40
  ad33bb:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad33c0:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad33c7:	ff ff 
  ad33c9:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad33ce:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad33d2:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad33d7:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad33dc:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad33e1:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad33e6:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad33ed:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad33f4:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad33fa:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3401:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3406:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad340d:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3412:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3419:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad341e:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3424:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3429:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad342e:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3433:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3439:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad343e:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3443:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3448:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad344e:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3453:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3458:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad345d:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3462:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3467:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad346c:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3472:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3477:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad347c:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3481:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad3487:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad348c:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3491:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3496:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad349c:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad34a1:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad34a6:	48 83 c7 40          	add    rdi,0x40
  ad34aa:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad34af:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad34b6:	ff ff 
  ad34b8:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad34bd:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad34c1:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad34c6:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad34cb:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad34d0:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad34d5:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad34dc:	48 ff c8             	dec    rax
  ad34df:	0f 85 3b fc ff ff    	jne    ad3120 <dgemm_kernel_HASWELL+0x520>
  ad34e5:	0f 18 4c 24 30       	prefetcht0 BYTE PTR [rsp+0x30]
  ad34ea:	41 0f 18 0f          	prefetcht0 BYTE PTR [r15]
  ad34ee:	41 0f 18 4f 18       	prefetcht0 BYTE PTR [r15+0x18]
  ad34f3:	43 0f 18 0c 97       	prefetcht0 BYTE PTR [r15+r10*4]
  ad34f8:	43 0f 18 4c 97 18    	prefetcht0 BYTE PTR [r15+r10*4+0x18]
  ad34fe:	43 0f 18 0c d7       	prefetcht0 BYTE PTR [r15+r10*8]
  ad3503:	43 0f 18 4c d7 18    	prefetcht0 BYTE PTR [r15+r10*8+0x18]
  ad3509:	4d 01 d7             	add    r15,r10
  ad350c:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3513:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3519:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3520:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3525:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad352c:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3531:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3538:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad353d:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3543:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3548:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad354d:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3552:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3558:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad355d:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3562:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3567:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad356d:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3572:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3577:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad357c:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3581:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3586:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad358b:	41 0f 18 0f          	prefetcht0 BYTE PTR [r15]
  ad358f:	41 0f 18 4f 18       	prefetcht0 BYTE PTR [r15+0x18]
  ad3594:	43 0f 18 0c 97       	prefetcht0 BYTE PTR [r15+r10*4]
  ad3599:	43 0f 18 4c 97 18    	prefetcht0 BYTE PTR [r15+r10*4+0x18]
  ad359f:	43 0f 18 0c d7       	prefetcht0 BYTE PTR [r15+r10*8]
  ad35a4:	43 0f 18 4c d7 18    	prefetcht0 BYTE PTR [r15+r10*8+0x18]
  ad35aa:	4f 8d 3c 57          	lea    r15,[r15+r10*2]
  ad35ae:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad35b4:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad35b9:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad35be:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad35c3:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad35c9:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad35ce:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad35d3:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad35d8:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad35de:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad35e3:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad35e8:	48 83 c7 40          	add    rdi,0x40
  ad35ec:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad35f1:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad35f8:	ff ff 
  ad35fa:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad35ff:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3603:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3608:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad360d:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3612:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3617:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad361e:	41 0f 18 0f          	prefetcht0 BYTE PTR [r15]
  ad3622:	41 0f 18 4f 18       	prefetcht0 BYTE PTR [r15+0x18]
  ad3627:	43 0f 18 0c 97       	prefetcht0 BYTE PTR [r15+r10*4]
  ad362c:	43 0f 18 4c 97 18    	prefetcht0 BYTE PTR [r15+r10*4+0x18]
  ad3632:	43 0f 18 0c d7       	prefetcht0 BYTE PTR [r15+r10*8]
  ad3637:	43 0f 18 4c d7 18    	prefetcht0 BYTE PTR [r15+r10*8+0x18]
  ad363d:	4d 29 d7             	sub    r15,r10
  ad3640:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3647:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad364d:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3654:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3659:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3660:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3665:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad366c:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3671:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3677:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad367c:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3681:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3686:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad368c:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3691:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3696:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad369b:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad36a1:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad36a6:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad36ab:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad36b0:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad36b5:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad36ba:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad36bf:	41 0f 18 0f          	prefetcht0 BYTE PTR [r15]
  ad36c3:	41 0f 18 4f 18       	prefetcht0 BYTE PTR [r15+0x18]
  ad36c8:	43 0f 18 0c 97       	prefetcht0 BYTE PTR [r15+r10*4]
  ad36cd:	43 0f 18 4c 97 18    	prefetcht0 BYTE PTR [r15+r10*4+0x18]
  ad36d3:	43 0f 18 0c d7       	prefetcht0 BYTE PTR [r15+r10*8]
  ad36d8:	43 0f 18 4c d7 18    	prefetcht0 BYTE PTR [r15+r10*8+0x18]
  ad36de:	4d 29 d7             	sub    r15,r10
  ad36e1:	4d 29 d7             	sub    r15,r10
  ad36e4:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad36ea:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad36ef:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad36f4:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad36f9:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad36ff:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3704:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3709:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad370e:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad3714:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3719:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad371e:	48 83 c7 40          	add    rdi,0x40
  ad3722:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3727:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad372e:	ff ff 
  ad3730:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3735:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3739:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad373e:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad3743:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3748:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad374d:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad3754:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad375b:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3761:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3768:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad376d:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3774:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3779:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3780:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3785:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad378b:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3790:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3795:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad379a:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad37a0:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad37a5:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad37aa:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad37af:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad37b5:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad37ba:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad37bf:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad37c4:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad37c9:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad37ce:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad37d3:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad37d9:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad37de:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad37e3:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad37e8:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad37ee:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad37f3:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad37f8:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad37fd:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad3803:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3808:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad380d:	48 83 c7 40          	add    rdi,0x40
  ad3811:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3816:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad381d:	ff ff 
  ad381f:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3824:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3828:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad382d:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad3832:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3837:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad383c:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad3843:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad384a:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3850:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3857:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad385c:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3863:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3868:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad386f:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3874:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad387a:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad387f:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3884:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3889:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad388f:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3894:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3899:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad389e:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad38a4:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad38a9:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad38ae:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad38b3:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad38b8:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad38bd:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad38c2:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad38c8:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad38cd:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad38d2:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad38d7:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad38dd:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad38e2:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad38e7:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad38ec:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad38f2:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad38f7:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad38fc:	48 83 c7 40          	add    rdi,0x40
  ad3900:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3905:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad390c:	ff ff 
  ad390e:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3913:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3918:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad391d:	48 83 c6 60          	add    rsi,0x60
  ad3921:	e9 06 04 00 00       	jmp    ad3d2c <dgemm_kernel_HASWELL+0x112c>
  ad3926:	48 a9 01 00 00 00    	test   rax,0x1
  ad392c:	0f 84 c2 03 00 00    	je     ad3cf4 <dgemm_kernel_HASWELL+0x10f4>
  ad3932:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3939:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad393e:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3945:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad394b:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3952:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3957:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad395e:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad3963:	c5 f5 59 e0          	vmulpd ymm4,ymm1,ymm0
  ad3967:	0f 18 8e 60 01 00 00 	prefetcht0 BYTE PTR [rsi+0x160]
  ad396e:	c5 6d 59 c0          	vmulpd ymm8,ymm2,ymm0
  ad3972:	c5 65 59 e0          	vmulpd ymm12,ymm3,ymm0
  ad3976:	0f 18 8e a0 01 00 00 	prefetcht0 BYTE PTR [rsi+0x1a0]
  ad397d:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3983:	c5 f5 59 e8          	vmulpd ymm5,ymm1,ymm0
  ad3987:	c5 6d 59 c8          	vmulpd ymm9,ymm2,ymm0
  ad398b:	c5 65 59 e8          	vmulpd ymm13,ymm3,ymm0
  ad398f:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3995:	c5 f5 59 f0          	vmulpd ymm6,ymm1,ymm0
  ad3999:	c5 6d 59 d0          	vmulpd ymm10,ymm2,ymm0
  ad399d:	48 83 c6 60          	add    rsi,0x60
  ad39a1:	c5 65 59 f0          	vmulpd ymm14,ymm3,ymm0
  ad39a5:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad39ab:	c5 f5 59 f8          	vmulpd ymm7,ymm1,ymm0
  ad39af:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad39b4:	c5 6d 59 d8          	vmulpd ymm11,ymm2,ymm0
  ad39b8:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad39bd:	c5 65 59 f8          	vmulpd ymm15,ymm3,ymm0
  ad39c1:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad39c6:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad39cc:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad39d1:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad39d6:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad39db:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad39e1:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad39e6:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad39eb:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad39f0:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad39f6:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad39fb:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3a00:	48 83 c7 40          	add    rdi,0x40
  ad3a04:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3a09:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad3a10:	ff ff 
  ad3a12:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3a17:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3a1b:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3a20:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad3a25:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3a2a:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3a2f:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad3a36:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3a3d:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3a43:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3a4a:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3a4f:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3a56:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3a5b:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3a62:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3a67:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3a6d:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3a72:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3a77:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3a7c:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3a82:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3a87:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3a8c:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3a91:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3a97:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3a9c:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3aa1:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3aa6:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3aab:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3ab0:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad3ab5:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3abb:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3ac0:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3ac5:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3aca:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad3ad0:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3ad5:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3ada:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3adf:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad3ae5:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3aea:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3aef:	48 83 c7 40          	add    rdi,0x40
  ad3af3:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3af8:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad3aff:	ff ff 
  ad3b01:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3b06:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3b0a:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3b0f:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad3b14:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3b19:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3b1e:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad3b25:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3b2c:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3b32:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3b39:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3b3e:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3b45:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3b4a:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3b51:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3b56:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3b5c:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3b61:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3b66:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3b6b:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3b71:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3b76:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3b7b:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3b80:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3b86:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3b8b:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3b90:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3b95:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3b9a:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3b9f:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad3ba4:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3baa:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3baf:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3bb4:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3bb9:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad3bbf:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3bc4:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3bc9:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3bce:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad3bd4:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3bd9:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3bde:	48 83 c7 40          	add    rdi,0x40
  ad3be2:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3be7:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad3bee:	ff ff 
  ad3bf0:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3bf5:	c5 fc 10 0e          	vmovups ymm1,YMMWORD PTR [rsi]
  ad3bf9:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3bfe:	c5 fc 10 56 20       	vmovups ymm2,YMMWORD PTR [rsi+0x20]
  ad3c03:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3c08:	c5 fc 10 5e 40       	vmovups ymm3,YMMWORD PTR [rsi+0x40]
  ad3c0d:	48 81 c6 c0 00 00 00 	add    rsi,0xc0
  ad3c14:	0f 18 8f 00 02 00 00 	prefetcht0 BYTE PTR [rdi+0x200]
  ad3c1b:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3c21:	0f 18 8e a0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xa0]
  ad3c28:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3c2d:	0f 18 8e e0 00 00 00 	prefetcht0 BYTE PTR [rsi+0xe0]
  ad3c34:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3c39:	0f 18 8e 20 01 00 00 	prefetcht0 BYTE PTR [rsi+0x120]
  ad3c40:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3c45:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3c4b:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3c50:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3c55:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3c5a:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3c60:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3c65:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3c6a:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3c6f:	c4 e2 7d 19 47 98    	vbroadcastsd ymm0,QWORD PTR [rdi-0x68]
  ad3c75:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3c7a:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3c7f:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3c84:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3c89:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3c8e:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad3c93:	c4 e2 7d 19 47 a0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x60]
  ad3c99:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3c9e:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3ca3:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3ca8:	c4 e2 7d 19 47 a8    	vbroadcastsd ymm0,QWORD PTR [rdi-0x58]
  ad3cae:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3cb3:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3cb8:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3cbd:	c4 e2 7d 19 47 b0    	vbroadcastsd ymm0,QWORD PTR [rdi-0x50]
  ad3cc3:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3cc8:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3ccd:	48 83 c7 40          	add    rdi,0x40
  ad3cd1:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3cd6:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad3cdd:	ff ff 
  ad3cdf:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3ce4:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3ce9:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3cee:	48 83 c6 60          	add    rsi,0x60
  ad3cf2:	eb 38                	jmp    ad3d2c <dgemm_kernel_HASWELL+0x112c>
  ad3cf4:	c5 dd 57 e4          	vxorpd ymm4,ymm4,ymm4
  ad3cf8:	c5 d5 57 ed          	vxorpd ymm5,ymm5,ymm5
  ad3cfc:	c5 cd 57 f6          	vxorpd ymm6,ymm6,ymm6
  ad3d00:	c5 c5 57 ff          	vxorpd ymm7,ymm7,ymm7
  ad3d04:	c4 41 3d 57 c0       	vxorpd ymm8,ymm8,ymm8
  ad3d09:	c4 41 35 57 c9       	vxorpd ymm9,ymm9,ymm9
  ad3d0e:	c4 41 2d 57 d2       	vxorpd ymm10,ymm10,ymm10
  ad3d13:	c4 41 25 57 db       	vxorpd ymm11,ymm11,ymm11
  ad3d18:	c4 41 1d 57 e4       	vxorpd ymm12,ymm12,ymm12
  ad3d1d:	c4 41 15 57 ed       	vxorpd ymm13,ymm13,ymm13
  ad3d22:	c4 41 0d 57 f6       	vxorpd ymm14,ymm14,ymm14
  ad3d27:	c4 41 05 57 ff       	vxorpd ymm15,ymm15,ymm15
  ad3d2c:	4c 89 e0             	mov    rax,r12
  ad3d2f:	48 83 e0 07          	and    rax,0x7
  ad3d33:	0f 84 87 00 00 00    	je     ad3dc0 <dgemm_kernel_HASWELL+0x11c0>
  ad3d39:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
  ad3d40:	c5 fc 10 4e a0       	vmovups ymm1,YMMWORD PTR [rsi-0x60]
  ad3d45:	c4 e2 7d 19 47 80    	vbroadcastsd ymm0,QWORD PTR [rdi-0x80]
  ad3d4b:	c4 e2 f5 b8 e0       	vfmadd231pd ymm4,ymm1,ymm0
  ad3d50:	c5 fc 10 56 c0       	vmovups ymm2,YMMWORD PTR [rsi-0x40]
  ad3d55:	c4 62 ed b8 c0       	vfmadd231pd ymm8,ymm2,ymm0
  ad3d5a:	c5 fc 10 5e e0       	vmovups ymm3,YMMWORD PTR [rsi-0x20]
  ad3d5f:	c4 62 e5 b8 e0       	vfmadd231pd ymm12,ymm3,ymm0
  ad3d64:	c4 e2 7d 19 47 88    	vbroadcastsd ymm0,QWORD PTR [rdi-0x78]
  ad3d6a:	c4 e2 f5 b8 e8       	vfmadd231pd ymm5,ymm1,ymm0
  ad3d6f:	c4 62 ed b8 c8       	vfmadd231pd ymm9,ymm2,ymm0
  ad3d74:	48 83 c6 60          	add    rsi,0x60
  ad3d78:	c4 62 e5 b8 e8       	vfmadd231pd ymm13,ymm3,ymm0
  ad3d7d:	c4 e2 7d 19 47 90    	vbroadcastsd ymm0,QWORD PTR [rdi-0x70]
  ad3d83:	c4 e2 f5 b8 f0       	vfmadd231pd ymm6,ymm1,ymm0
  ad3d88:	c4 62 ed b8 d0       	vfmadd231pd ymm10,ymm2,ymm0
  ad3d8d:	48 83 c7 20          	add    rdi,0x20
  ad3d91:	c4 62 e5 b8 f0       	vfmadd231pd ymm14,ymm3,ymm0
  ad3d96:	c4 e2 7d 19 87 78 ff 	vbroadcastsd ymm0,QWORD PTR [rdi-0x88]
  ad3d9d:	ff ff 
  ad3d9f:	c4 e2 f5 b8 f8       	vfmadd231pd ymm7,ymm1,ymm0
  ad3da4:	c4 62 ed b8 d8       	vfmadd231pd ymm11,ymm2,ymm0
  ad3da9:	c4 62 e5 b8 f8       	vfmadd231pd ymm15,ymm3,ymm0
  ad3dae:	48 ff c8             	dec    rax
  ad3db1:	75 8d                	jne    ad3d40 <dgemm_kernel_HASWELL+0x1140>
  ad3db3:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  ad3dba:	00 00 00 
  ad3dbd:	0f 1f 00             	nop    DWORD PTR [rax]
  ad3dc0:	0f 18 8c 24 80 00 00 	prefetcht0 BYTE PTR [rsp+0x80]
  ad3dc7:	00 
  ad3dc8:	c4 e2 7d 19 44 24 30 	vbroadcastsd ymm0,QWORD PTR [rsp+0x30]
  ad3dcf:	c5 dd 59 e0          	vmulpd ymm4,ymm4,ymm0
  ad3dd3:	c5 d5 59 e8          	vmulpd ymm5,ymm5,ymm0
  ad3dd7:	c5 cd 59 f0          	vmulpd ymm6,ymm6,ymm0
  ad3ddb:	c5 c5 59 f8          	vmulpd ymm7,ymm7,ymm0
  ad3ddf:	0f 18 8c 24 c0 00 00 	prefetcht0 BYTE PTR [rsp+0xc0]
  ad3de6:	00 
  ad3de7:	c5 3d 59 c0          	vmulpd ymm8,ymm8,ymm0
  ad3deb:	c5 35 59 c8          	vmulpd ymm9,ymm9,ymm0
  ad3def:	c5 2d 59 d0          	vmulpd ymm10,ymm10,ymm0
  ad3df3:	c5 25 59 d8          	vmulpd ymm11,ymm11,ymm0
  ad3df7:	0f 18 8c 24 00 01 00 	prefetcht0 BYTE PTR [rsp+0x100]
  ad3dfe:	00 
  ad3dff:	c5 1d 59 e0          	vmulpd ymm12,ymm12,ymm0
  ad3e03:	c5 15 59 e8          	vmulpd ymm13,ymm13,ymm0
  ad3e07:	c5 0d 59 f0          	vmulpd ymm14,ymm14,ymm0
  ad3e0b:	c5 05 59 f8          	vmulpd ymm15,ymm15,ymm0
  ad3e0f:	0f 18 8c 24 40 01 00 	prefetcht0 BYTE PTR [rsp+0x140]
  ad3e16:	00 
  ad3e17:	c4 e3 5d 06 c6 20    	vperm2f128 ymm0,ymm4,ymm6,0x20
  ad3e1d:	c4 e3 55 06 cf 20    	vperm2f128 ymm1,ymm5,ymm7,0x20
  ad3e23:	c4 e3 5d 06 d6 31    	vperm2f128 ymm2,ymm4,ymm6,0x31
  ad3e29:	c4 e3 55 06 df 31    	vperm2f128 ymm3,ymm5,ymm7,0x31
  ad3e2f:	c5 fd 14 e1          	vunpcklpd ymm4,ymm0,ymm1
  ad3e33:	c5 fd 15 e9          	vunpckhpd ymm5,ymm0,ymm1
  ad3e37:	c5 ed 14 f3          	vunpcklpd ymm6,ymm2,ymm3
  ad3e3b:	c5 ed 15 fb          	vunpckhpd ymm7,ymm2,ymm3
  ad3e3f:	4b 8d 04 57          	lea    rax,[r15+r10*2]
  ad3e43:	c4 c1 5d 58 27       	vaddpd ymm4,ymm4,YMMWORD PTR [r15]
  ad3e48:	c4 81 55 58 2c 17    	vaddpd ymm5,ymm5,YMMWORD PTR [r15+r10*1]
  ad3e4e:	c5 cd 58 30          	vaddpd ymm6,ymm6,YMMWORD PTR [rax]
  ad3e52:	c4 a1 45 58 3c 10    	vaddpd ymm7,ymm7,YMMWORD PTR [rax+r10*1]
  ad3e58:	c4 c1 7c 11 27       	vmovups YMMWORD PTR [r15],ymm4
  ad3e5d:	c4 81 7c 11 2c 17    	vmovups YMMWORD PTR [r15+r10*1],ymm5
  ad3e63:	c5 fc 11 30          	vmovups YMMWORD PTR [rax],ymm6
  ad3e67:	c4 a1 7c 11 3c 10    	vmovups YMMWORD PTR [rax+r10*1],ymm7
  ad3e6d:	41 0f 18 57 38       	prefetcht1 BYTE PTR [r15+0x38]
  ad3e72:	43 0f 18 54 17 38    	prefetcht1 BYTE PTR [r15+r10*1+0x38]
  ad3e78:	0f 18 50 38          	prefetcht1 BYTE PTR [rax+0x38]
  ad3e7c:	42 0f 18 54 10 38    	prefetcht1 BYTE PTR [rax+r10*1+0x38]
  ad3e82:	c4 c3 3d 06 c2 20    	vperm2f128 ymm0,ymm8,ymm10,0x20
  ad3e88:	c4 c3 35 06 cb 20    	vperm2f128 ymm1,ymm9,ymm11,0x20
  ad3e8e:	c4 c3 3d 06 d2 31    	vperm2f128 ymm2,ymm8,ymm10,0x31
  ad3e94:	c4 c3 35 06 db 31    	vperm2f128 ymm3,ymm9,ymm11,0x31
  ad3e9a:	c5 fd 14 e1          	vunpcklpd ymm4,ymm0,ymm1
  ad3e9e:	c5 fd 15 e9          	vunpckhpd ymm5,ymm0,ymm1
  ad3ea2:	c5 ed 14 f3          	vunpcklpd ymm6,ymm2,ymm3
  ad3ea6:	c5 ed 15 fb          	vunpckhpd ymm7,ymm2,ymm3
  ad3eaa:	4a 8d 04 50          	lea    rax,[rax+r10*2]
  ad3eae:	4a 8d 2c 50          	lea    rbp,[rax+r10*2]
  ad3eb2:	c5 dd 58 20          	vaddpd ymm4,ymm4,YMMWORD PTR [rax]
  ad3eb6:	c4 a1 55 58 2c 10    	vaddpd ymm5,ymm5,YMMWORD PTR [rax+r10*1]
  ad3ebc:	c5 cd 58 75 00       	vaddpd ymm6,ymm6,YMMWORD PTR [rbp+0x0]
  ad3ec1:	c4 a1 45 58 7c 15 00 	vaddpd ymm7,ymm7,YMMWORD PTR [rbp+r10*1+0x0]
  ad3ec8:	c5 fc 11 20          	vmovups YMMWORD PTR [rax],ymm4
  ad3ecc:	c4 a1 7c 11 2c 10    	vmovups YMMWORD PTR [rax+r10*1],ymm5
  ad3ed2:	c5 fc 11 75 00       	vmovups YMMWORD PTR [rbp+0x0],ymm6
  ad3ed7:	c4 a1 7c 11 7c 15 00 	vmovups YMMWORD PTR [rbp+r10*1+0x0],ymm7
  ad3ede:	0f 18 50 38          	prefetcht1 BYTE PTR [rax+0x38]
  ad3ee2:	42 0f 18 54 10 38    	prefetcht1 BYTE PTR [rax+r10*1+0x38]
  ad3ee8:	0f 18 55 38          	prefetcht1 BYTE PTR [rbp+0x38]
  ad3eec:	42 0f 18 54 15 38    	prefetcht1 BYTE PTR [rbp+r10*1+0x38]
  ad3ef2:	c4 c3 1d 06 c6 20    	vperm2f128 ymm0,ymm12,ymm14,0x20
  ad3ef8:	c4 c3 15 06 cf 20    	vperm2f128 ymm1,ymm13,ymm15,0x20
  ad3efe:	c4 c3 1d 06 d6 31    	vperm2f128 ymm2,ymm12,ymm14,0x31
  ad3f04:	c4 c3 15 06 df 31    	vperm2f128 ymm3,ymm13,ymm15,0x31
  ad3f0a:	c5 fd 14 e1          	vunpcklpd ymm4,ymm0,ymm1
  ad3f0e:	c5 fd 15 e9          	vunpckhpd ymm5,ymm0,ymm1
  ad3f12:	c5 ed 14 f3          	vunpcklpd ymm6,ymm2,ymm3
  ad3f16:	c5 ed 15 fb          	vunpckhpd ymm7,ymm2,ymm3
  ad3f1a:	4a 8d 04 90          	lea    rax,[rax+r10*4]
  ad3f1e:	4a 8d 6c 95 00       	lea    rbp,[rbp+r10*4+0x0]
  ad3f23:	c5 dd 58 20          	vaddpd ymm4,ymm4,YMMWORD PTR [rax]
  ad3f27:	c4 a1 55 58 2c 10    	vaddpd ymm5,ymm5,YMMWORD PTR [rax+r10*1]
  ad3f2d:	c5 cd 58 75 00       	vaddpd ymm6,ymm6,YMMWORD PTR [rbp+0x0]
  ad3f32:	c4 a1 45 58 7c 15 00 	vaddpd ymm7,ymm7,YMMWORD PTR [rbp+r10*1+0x0]
  ad3f39:	c5 fc 11 20          	vmovups YMMWORD PTR [rax],ymm4
  ad3f3d:	c4 a1 7c 11 2c 10    	vmovups YMMWORD PTR [rax+r10*1],ymm5
  ad3f43:	c5 fc 11 75 00       	vmovups YMMWORD PTR [rbp+0x0],ymm6
  ad3f48:	c4 a1 7c 11 7c 15 00 	vmovups YMMWORD PTR [rbp+r10*1+0x0],ymm7
  ad3f4f:	0f 18 50 38          	prefetcht1 BYTE PTR [rax+0x38]
  ad3f53:	42 0f 18 54 10 38    	prefetcht1 BYTE PTR [rax+r10*1+0x38]
  ad3f59:	0f 18 55 38          	prefetcht1 BYTE PTR [rbp+0x38]
  ad3f5d:	42 0f 18 54 15 38    	prefetcht1 BYTE PTR [rbp+r10*1+0x38]
  ad3f63:	49 83 c7 20          	add    r15,0x20
  ad3f67:	49 c1 e4 03          	shl    r12,0x3
  ad3f6b:	41 0f 18 58 20       	prefetcht2 BYTE PTR [r8+0x20]
  ad3f70:	43 0f 18 5c e0 20    	prefetcht2 BYTE PTR [r8+r12*8+0x20]
  ad3f76:	41 0f 18 58 60       	prefetcht2 BYTE PTR [r8+0x60]
  ad3f7b:	43 0f 18 5c e0 60    	prefetcht2 BYTE PTR [r8+r12*8+0x60]
  ad3f81:	49 81 c0 80 00 00 00 	add    r8,0x80
  ad3f88:	49 c1 fc 03          	sar    r12,0x3
  ad3f8c:	49 ff cb             	dec    r11
  ad3f8f:	0f 85 7b ed ff ff    	jne    ad2d10 <dgemm_kernel_HASWELL+0x110>
  ad3f95:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  ad3f9c:	00 00 00 
  ad3f9f:	90                   	nop
  ad3fa0:	4d 89 eb             	mov    r11,r13
  ad3fa3:	49 c1 fb 02          	sar    r11,0x2
  ad3fa7:	49 c1 e3 07          	shl    r11,0x7
  ad3fab:	4d 29 d8             	sub    r8,r11
  ad3fae:	49 f7 c5 03 00 00 00 	test   r13,0x3
  ad3fb5:	0f 84 65 0c 00 00    	je     ad4c20 <dgemm_kernel_HASWELL+0x2020>
  ad3fbb:	49 f7 c5 02 00 00 00 	test   r13,0x2
  ad3fc2:	0f 84 28 06 00 00    	je     ad45f0 <dgemm_kernel_HASWELL+0x19f0>
  ad3fc8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  ad3fcf:	00 
  ad3fd0:	48 8d b4 24 80 00 00 	lea    rsi,[rsp+0x80]
  ad3fd7:	00 
  ad3fd8:	48 83 c6 60          	add    rsi,0x60
  ad3fdc:	c5 d9 57 e4          	vxorpd xmm4,xmm4,xmm4
  ad3fe0:	c5 d1 57 ed          	vxorpd xmm5,xmm5,xmm5
  ad3fe4:	c5 c9 57 f6          	vxorpd xmm6,xmm6,xmm6
  ad3fe8:	c5 c1 57 ff          	vxorpd xmm7,xmm7,xmm7
  ad3fec:	c4 41 39 57 c0       	vxorpd xmm8,xmm8,xmm8
  ad3ff1:	c4 41 31 57 c9       	vxorpd xmm9,xmm9,xmm9
  ad3ff6:	c4 41 29 57 d2       	vxorpd xmm10,xmm10,xmm10
  ad3ffb:	c4 41 21 57 db       	vxorpd xmm11,xmm11,xmm11
  ad4000:	c4 41 19 57 e4       	vxorpd xmm12,xmm12,xmm12
  ad4005:	c4 41 11 57 ed       	vxorpd xmm13,xmm13,xmm13
  ad400a:	c4 41 09 57 f6       	vxorpd xmm14,xmm14,xmm14
  ad400f:	c4 41 01 57 ff       	vxorpd xmm15,xmm15,xmm15
  ad4014:	4c 89 e0             	mov    rax,r12
  ad4017:	48 c1 f8 03          	sar    rax,0x3
  ad401b:	0f 84 4f 04 00 00    	je     ad4470 <dgemm_kernel_HASWELL+0x1870>
  ad4021:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  ad4028:	00 00 00 
  ad402b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  ad4030:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad4035:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad403a:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad403f:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad4044:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad4049:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad404e:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad4053:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad4058:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad405d:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad4062:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad4067:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad406c:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad4071:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad4076:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad407b:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad4080:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad4085:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad408a:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad408f:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad4094:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad4099:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad409e:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad40a3:	48 83 c6 60          	add    rsi,0x60
  ad40a7:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad40ac:	48 83 c7 10          	add    rdi,0x10
  ad40b0:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad40b5:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad40ba:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad40bf:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad40c4:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad40c9:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad40ce:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad40d3:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad40d8:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad40dd:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad40e2:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad40e7:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad40ec:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad40f1:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad40f6:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad40fb:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad4100:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad4105:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad410a:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad410f:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad4114:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad4119:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad411e:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad4123:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad4128:	48 83 c6 60          	add    rsi,0x60
  ad412c:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad4131:	48 83 c7 10          	add    rdi,0x10
  ad4135:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad413a:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad413f:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad4144:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad4149:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad414e:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad4153:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad4158:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad415d:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad4162:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad4167:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad416c:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad4171:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad4176:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad417b:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad4180:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad4185:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad418a:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad418f:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad4194:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad4199:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad419e:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad41a3:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad41a8:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad41ad:	48 83 c6 60          	add    rsi,0x60
  ad41b1:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad41b6:	48 83 c7 10          	add    rdi,0x10
  ad41ba:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad41bf:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad41c4:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad41c9:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad41ce:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad41d3:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad41d8:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad41dd:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad41e2:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad41e7:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad41ec:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad41f1:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad41f6:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad41fb:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad4200:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad4205:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad420a:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad420f:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad4214:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad4219:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad421e:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad4223:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad4228:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad422d:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad4232:	48 83 c6 60          	add    rsi,0x60
  ad4236:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad423b:	48 83 c7 10          	add    rdi,0x10
  ad423f:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad4244:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad4249:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad424e:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad4253:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad4258:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad425d:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad4262:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad4267:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad426c:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad4271:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad4276:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad427b:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad4280:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad4285:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad428a:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad428f:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad4294:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad4299:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad429e:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad42a3:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad42a8:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad42ad:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad42b2:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad42b7:	48 83 c6 60          	add    rsi,0x60
  ad42bb:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad42c0:	48 83 c7 10          	add    rdi,0x10
  ad42c4:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad42c9:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad42ce:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad42d3:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad42d8:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad42dd:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad42e2:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad42e7:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad42ec:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad42f1:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad42f6:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad42fb:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad4300:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad4305:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad430a:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad430f:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad4314:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad4319:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad431e:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad4323:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad4328:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad432d:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad4332:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad4337:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad433c:	48 83 c6 60          	add    rsi,0x60
  ad4340:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0
  ad4345:	48 83 c7 10          	add    rdi,0x10
  ad4349:	c4 62 e1 b8 f8       	vfmadd231pd xmm15,xmm3,xmm0
  ad434e:	c5 f8 10 47 80       	vmovups xmm0,XMMWORD PTR [rdi-0x80]
  ad4353:	c5 fb 12 4e a0       	vmovddup xmm1,QWORD PTR [rsi-0x60]
  ad4358:	c5 fb 12 56 a8       	vmovddup xmm2,QWORD PTR [rsi-0x58]
  ad435d:	c5 fb 12 5e b0       	vmovddup xmm3,QWORD PTR [rsi-0x50]
  ad4362:	c4 e2 f1 b8 e0       	vfmadd231pd xmm4,xmm1,xmm0
  ad4367:	c5 fb 12 4e b8       	vmovddup xmm1,QWORD PTR [rsi-0x48]
  ad436c:	c4 e2 e9 b8 e8       	vfmadd231pd xmm5,xmm2,xmm0
  ad4371:	c5 fb 12 56 c0       	vmovddup xmm2,QWORD PTR [rsi-0x40]
  ad4376:	c4 e2 e1 b8 f0       	vfmadd231pd xmm6,xmm3,xmm0
  ad437b:	c5 fb 12 5e c8       	vmovddup xmm3,QWORD PTR [rsi-0x38]
  ad4380:	c4 e2 f1 b8 f8       	vfmadd231pd xmm7,xmm1,xmm0
  ad4385:	c5 fb 12 4e d0       	vmovddup xmm1,QWORD PTR [rsi-0x30]
  ad438a:	c4 62 e9 b8 c0       	vfmadd231pd xmm8,xmm2,xmm0
  ad438f:	c5 fb 12 56 d8       	vmovddup xmm2,QWORD PTR [rsi-0x28]
  ad4394:	c4 62 e1 b8 c8       	vfmadd231pd xmm9,xmm3,xmm0
  ad4399:	c5 fb 12 5e e0       	vmovddup xmm3,QWORD PTR [rsi-0x20]
  ad439e:	c4 62 f1 b8 d0       	vfmadd231pd xmm10,xmm1,xmm0
  ad43a3:	c5 fb 12 4e e8       	vmovddup xmm1,QWORD PTR [rsi-0x18]
  ad43a8:	c4 62 e9 b8 d8       	vfmadd231pd xmm11,xmm2,xmm0
  ad43ad:	c5 fb 12 56 f0       	vmovddup xmm2,QWORD PTR [rsi-0x10]
  ad43b2:	c4 62 e1 b8 e0       	vfmadd231pd xmm12,xmm3,xmm0
  ad43b7:	c5 fb 12 5e f8       	vmovddup xmm3,QWORD PTR [rsi-0x8]
  ad43bc:	c4 62 f1 b8 e8       	vfmadd231pd xmm13,xmm1,xmm0
  ad43c1:	48 83 c6 60          	add    rsi,0x60
  ad43c5:	c4 62 e9 b8 f0       	vfmadd231pd xmm14,xmm2,xmm0