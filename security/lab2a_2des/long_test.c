#include <stdio.h>

int main() {
    long a = 1000L*1000*1000*10;
    printf("%lld\n", a);
    printf("%d, %d\n", sizeof(int), sizeof(long));
}