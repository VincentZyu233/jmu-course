double fun(int i){
    volatile double d[1] = {3.14};
    volatile long int a[2];
    a[i] = 0x40000000;
    return d[0];
}

/*

gcc -S -O0 fun.c
gcc -S -O2 fun.c

*/