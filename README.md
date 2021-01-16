# lldb-peda
gdb-peda for lldb.
Documentation for the lldb API can be found from this link: https://lldb.llvm.org/python_reference/

## how to use
Execute this command inside lldb
```
(lldb)command script import reverse.py
```

If you want to enable this command whenever lldb is used, then execute this command below
```
$ cp reverse.py ~
$ echo "command script import  ~/reverse.py" >>$HOME/.lldbinit
```

## command
```
(lldb)reg
(lldb)code
(lldb)stack
(lldb)peda
```

## example

![Alt text](https://github.com/ryaoi/lldb-peda/blob/master/reg.png "Register")
![Alt text](https://github.com/ryaoi/lldb-peda/blob/master/code.png "Code")
![Alt text](https://github.com/ryaoi/lldb-peda/blob/master/stack.png "Stack")

peda command will output all of them


## Print other registers value with this script
Edit the reverse.py file.
Add more register name inside this variable.
```
OUTPUT_REGISTERS = [
    'rax',
    'rbx',
    'rcx',
    'rdx',
    'rsi',
    'rsi',
    'rdi',
    'rbp',
    'rsp',
    'rip'
]
```

These register are available
```
rax
rbx
rcx
rdx
rdi
rsi
rbp
rsp
r8
r9
r10
r11
r12
r13
r14
r15
rip
rflags
cs
fs
gs
eax
ebx
ecx
edx
edi
esi
ebp
esp
r8d
r9d
r10d
r11d
r12d
r13d
r14d
r15d
ax
bx
cx
dx
di
si
bp
sp
r8w
r9w
r10w
r11w
r12w
r13w
r14w
r15w
ah
bh
ch
dh
al
bl
cl
dl
dil
sil
bpl
spl
r8l
r9l
r10l
r11l
r12l
r13l
r14l
r15l
fctrl
fstat
ftag
fop
fioff
fiseg
fooff
foseg
mxcsr
mxcsrmask
stmm0
stmm1
stmm2
stmm3
stmm4
stmm5
stmm6
stmm7
ymm0
ymm1
ymm2
ymm3
ymm4
ymm5
ymm6
ymm7
ymm8
ymm9
ymm10
ymm11
ymm12
ymm13
ymm14
ymm15
xmm0
xmm1
xmm2
xmm3
xmm4
xmm5
xmm6
xmm7
xmm8
xmm9
xmm10
xmm11
xmm12
xmm13
xmm14
xmm15
trapno
err
faultvaddr
```
