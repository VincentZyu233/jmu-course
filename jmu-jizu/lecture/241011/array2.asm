section .data
    a dw 10, 15, 20, 25, 30          ; 初始化数组 a
    b dw 0, 0, 0, 0, 0                ; 初始化数组 b
    fmt db "b[%d] = %d", 10, 0        ; 输出格式字符串，10 是换行符

section .bss
    i resb 1                          ; 存储循环索引 i
    temp resb 2                       ; 临时存储结果

section .text
    global _start

_start:
    ; 使用指针遍历数组 a
    mov si, a                        ; si 指向数组 a 的起始地址
    mov di, b                        ; di 指向数组 b 的起始地址

    ; 循环操作
    mov cx, 5                        ; 设置循环次数为 5
loop_start:
    lodsw                            ; 加载 a[i] 到 ax
    mov bl, 5                        ; bl = 5
    xor dx, dx                       ; 清空 dx（用于除法）
    div bl                           ; ax = ax / bl，结果在 ax 中
    mov bl, 3                        ; bl = 3
    mul bl                           ; ax = ax * bl，结果在 ax 中
    stosw                            ; 将结果存储到 b[i]

    ; 更新循环索引 i
    inc byte [i]                    ; i++
    loop loop_start                  ; 循环

    ; 输出结果
    mov cx, 5                        ; 设置输出次数
    mov byte [i], 1                  ; 从 1 开始输出（b[1] 到 b[4]）
output_loop:
    movzx ax, word [di]             ; 将 b[i] 取到 ax
    push ax                          ; 保存 ax
    push dword [i]                  ; 推送索引
    push fmt                         ; 推送格式字符串
    call printf                      ; 调用 printf
    add esp, 12                      ; 清理堆栈
    inc byte [i]                    ; i++
    loop output_loop                 ; 输出下一个

    ; 退出程序
    mov eax, 1                       ; 系统调用号 (sys_exit)
    xor ebx, ebx                     ; 返回 0
    int 0x80                         ; 调用内核

; 声明外部函数
extern printf
