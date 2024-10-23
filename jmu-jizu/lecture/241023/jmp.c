int jmp(int a){
    int b;
    if ( a>100 ){
        a *= 2;
    } else if ( a>200 ) {
        a *= 3;
    } else {
        a *= 4;
    }
    b = a;
    return b;
}