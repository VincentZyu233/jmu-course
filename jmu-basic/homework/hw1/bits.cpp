#include <bits/stdc++.h>
using namespace std;

signed main(){
    long long a = 1891285101023;
    
    cout << "bits of a: \n";
    for ( int i=63; i>=0; i-- ){
        cout << ((a>>i) & 1);
        if ( (i)%4 == 0 ) cout << ' ';
        if ( (i)%16 == 0 ) cout << '\n';
    }
}

/*
g++ bits.cpp -o bits && ./bits
*/
