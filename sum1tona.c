#include<stdio.h>
int sum(int n){
    if(int n==1) return 1;
    return n+sum(n-1);
}
int main(){
    int n;
    printf("enter the number ");
    scanf("%d",&n);
    int a=sum(n);
    printf("%d",a);
    return 0;
}