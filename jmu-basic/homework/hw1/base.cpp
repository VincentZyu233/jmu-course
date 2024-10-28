#include <bits/stdc++.h>
using namespace std;

void print_in_base_t(int a, int t){
    while(a){
        cout << a%t;
        a /= t;
    }
}

int base_2_to_10(string s){
    int res = 0;
    int len = (int)s.size();
    for ( int i=1; i<=len; i++ ){
        char c = s[len-i];
        if ( c=='1' ){
            res += (1<<(i-1));
        }
    }
    return res;
}

signed main(){
    string s = "10101011";
    int a = base_2_to_10(s);
    cout << s << " in base 10 is: " << a << '\n';

    print_in_base_t(a,16);
}


/*
g++ base.cpp -o base && ./base
*/