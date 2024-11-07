#include <stdio.h>

signed main(){
    printf("hello");
}

/*

gcc -S program.c -o program.s

gcc -g -o file.o file.c
objdump -d file.o >> file.txt

vim ./file.txt

call puts
push $0x...... 吧内存地址压入stack

b main
r
x/10x 0x80484c0


 */
