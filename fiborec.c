#include<stdio.h>
int fibo(int a){
    if(a<=2) return 1;
    int ab = fibo(a-1) + fibo(a-2);
    return ab;

}
int main(){
    int a;
    printf("enter the valu : ");
    scanf("%d",&a);
    printf(" %d",fibo(a));
    return 0;
}