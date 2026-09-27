#include<stdio.h>
void swap(int *x, int *y){
    int a;
    a = *x;
    *x=*y;
    *y=a;
    return;
}
int main()
{
    int a=34,b=78;
    printf("%d and %d\n",a,b);
    swap(&a,&b);
    printf("%d and %d\n",a,b);
    return 0;    
}