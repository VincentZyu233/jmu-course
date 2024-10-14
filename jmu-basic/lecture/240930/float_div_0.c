extern int printf(const char* __restrict__format, ...);

int main(){
    printf("%lf", 1.0 / 0.0);
}