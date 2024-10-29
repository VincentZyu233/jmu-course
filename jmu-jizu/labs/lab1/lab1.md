# 课堂派实验一

## 数据在内存中的二进制表示实验


### 实验（实践）目的：加深学生对于数据在计算机内存中是如何进行二进制编码以及如何存放的认识。

### 实验（实践）要求：
（1）要求使用指针、内存操作和位操作形式，输出变量在内存中的存放形式，不可使用基于数值换算的二进制转换算法。（2）能够现场解释代码与实验结果。

### 实验（实践）内容：使用C语言，分别输出以下变量在内存中的二进制形式：
（1）一个int型的正数，（2）一个int型的负数，（3）一个float型的正数，（4）一个float型的负数，（5）一个char型的字符


### 代码

[bits.cpp](bits.cpp)

```cpp
/*
g++ bits.cpp -o bits && ./bits
*/

#include <bits/stdc++.h>
using namespace std;

template<typename T>
void print_bits( T a, size_t len ){
    cout << "bits of " << a << ": \n";
    long b = (long) a;
    for ( int i=(int)(len)-1; i>=0; i-- ){
        cout << ( (a>>i) & 1 );
        if (i%4==0) cout << ' ';
    }
    cout << "\n\n";
}


signed main() {
    printf("int: %zu bits\n", sizeof(int) * CHAR_BIT);
    printf("char: %zu bits\n", sizeof(char) * CHAR_BIT);
    printf("short: %zu bits\n", sizeof(short) * CHAR_BIT);
    printf("long: %zu bits\n", sizeof(long) * CHAR_BIT);
    printf("float: %zu bits\n", sizeof(float) * CHAR_BIT);
    printf("double: %zu bits\n", sizeof(double) * CHAR_BIT);

    // int a = 114514;
    // for ( int i=31; i>=0; i-- ){
    //     cout << ( (a>>i) & 1 );
    //     if ( i%4==0 ) cout << ' ';
    // }
    // cout << '\n';

    int a = 114514;
    int b = -1919810;
    float c = 3.14159265;
    float d = -5.55555;
    char e = 'A';

    print_bits((long)a, sizeof(int) * CHAR_BIT);
    print_bits((long)b, sizeof(int) * CHAR_BIT);
    print_bits((long)c, sizeof(float) * CHAR_BIT);
    print_bits((long)d, sizeof(float) * CHAR_BIT);
    print_bits((long)e, sizeof(char) * CHAR_BIT);

    return 0;
}

```

### 运行结果：

```bash

vincentzyu@vincentzyu:~/Documents/jmu-course/jmu-jizu/labs/lab1$ g++ bits.cpp -o bits && ./bits
int: 32 bits
char: 8 bits
short: 16 bits
long: 64 bits
float: 32 bits
double: 64 bits
bits of 114514: 
0000 0000 0000 0001 1011 1111 0101 0010 

bits of -1919810: 
1111 1111 1110 0010 1011 0100 1011 1110 

bits of 3: 
0000 0000 0000 0000 0000 0000 0000 0011 

bits of -5: 
1111 1111 1111 1111 1111 1111 1111 1011 

bits of 65: 
0100 0001 

vincentzyu@vincentzyu:~/Documents/jmu-course/jmu-jizu/labs/lab1$ 

```