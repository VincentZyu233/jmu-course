int foo(){
    short int a[5] = {10,15,20,25,30};
    short int b[5];
    for ( int i=0; i<5; i++ ){
        b[i] = a[i] / 5 * 3;
    }
}