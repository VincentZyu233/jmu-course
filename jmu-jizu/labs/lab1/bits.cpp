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
        cout << ( (b>>i) & 1 );
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