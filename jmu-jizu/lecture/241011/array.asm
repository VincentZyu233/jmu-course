section .data
a dw 10, 15, 20, 25, 30       ; 数组 a，5 个元素
b dw 0, 0, 0, 0, 0            ; 数组 b，用于存储结果

section .text
global _start

_start:
    mov cx, 5                  ; 循环次数
    mov si, a                  ; 源地址：数组 a 的起始地址
    mov di, b                  ; 目标地址：数组 b 的起始地址

loop_start:
    lodsw                       ; 加载 a 中的下一个元素到 AX
    mov bl, 5                   ; 将除数 5 加载到 BL
    div bl                      ; AX / BL，结果在 AL，余数在 AH

    mov bl, 3                   ; 将乘数 3 加载到 BL
    mul bl                      ; AL * BL，结果在 AX

    stosw                       ; 将 AX 中的结果存储到数组 b 中
    loop loop_start             ; 循环直到 CX 为 0

    ; 退出程序
    mov ax, 0x4c00              ; DOS 中断退出
    int 0x21
