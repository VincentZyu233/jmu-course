section .data
    a db 12h, 34h
    b dw 56h, 789Ah

section .text
global _start

_start:
    ; 在这里添加您的程序逻辑
    ; 例如：退出程序
    mov eax, 60     ; syscall: exit
    xor edi, edi    ; status: 0
    syscall          ; 调用内核
