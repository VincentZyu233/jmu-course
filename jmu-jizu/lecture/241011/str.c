int foo(){
    char *s = "hello world\0";
    int i;
    for ( int i=0; i<11; i++ ){
        if ( s[i]=='d') break;
    }
    return i;
}