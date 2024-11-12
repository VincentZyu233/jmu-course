/*
gcc -g -o gcd.o gcd.c
./gcd.o

*/

#include<stdio.h>

void main(){
    int tmp;
    int a,b;
    scanf("%d", &a);
    scanf("%d", &b);
    printf("gcd(%d, %d) = ", a, b);
    while(b){
        tmp = b;
        b = a%b;
        a = tmp;
    }
    printf("%d\n", a);
    getchar();
    getchar();
}
