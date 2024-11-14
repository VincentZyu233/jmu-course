# **集美大学计算机工程学院实验报告**

|**课程名称**：** |**班级**：软件2213|**实验成绩**：|
| :- | :- | :- |
|**指导教师**：王巍|**姓名**：张喻||
|**实验项目名称**：|**学号**：202221332097|**上机实践日期**：|
|**实验项目编号**：|**组号**：|**上机实践时间**： 2 学时|

![----------](black-line.png)

## **一、目的**

本次实验所涉及并要求掌握的知识点。

> (1)掌握  gcc  的用法； 
> (2)了解目标代码、库函数的使用； 
> (3)掌握静态库和共享库的构造与使用；


## **二、实验内容与设计思想**

1．设计思路

`     `2．主要数据结构

3．主要代码结构

`     `4．主要代码段分析

` `5．电路图（选）。


## **三、实验使用环境**

VMWare Ubuntu16-32bit 虚拟机
```bash
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4$ uname -a
Linux ubuntu 4.4.0-210-generic #242-Ubuntu SMP Fri Apr 16 09:57:00 UTC 2021 i686 i686 i686 GNU/Linux
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4$ 
```


## **四、实验步骤和调试过程**

### 1．实验步骤

#### gcd/gcd.c: 
```c
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

```

##### 运行：
```bash
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4$ cd gcd
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/gcd$ ls
gcd.c  gcd.o
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/gcd$ gcc -g -o gcd.o gcd.c
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/gcd$ ./gcd.o

15
20
gcd(15, 20) = 5
^C
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/gcd$ 

```

##### 然后把.o文件用objdump工具进行反汇编 输出到txt
```bash

wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/ubuntu16-32bit-vm/gcd$ ls
gcd.c  gcd.o
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/ubuntu16-32bit-vm/gcd$ objdump -d gcd.o >> gcd.o.txt
wang@ubuntu:/mnt/hgfs/jmu-course/jmu-basic/labs/lab4/ubuntu16-32bit-vm/gcd$ 

```

###### 阅读一下反汇编以后的代码

- main函数的入口，地址是080484
```asm
080484eb <main>:
80484eb: 8d 4c 24 04 lea 0x4(%esp),%ecx
80484ef: 83 e4 f0 and $0xfffffff0,%esp
```

`080484eb`是函数的起始地址
`<main>`是函数的标识符




2．测试数据设计

3．测试结果分析。


**五、实验小结**

1．实验中遇到的问题及解决过程

2．实验中产生的错误及原因分析

3．实验体会和收获。


**六、附录**

`    `参考文献和相关资料。

