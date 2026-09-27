#include<stdio.h>
void sum(int n,int a){
    if(n==0){
        printf("%d",a);
        return ;
    }
    sum(n-1,a+n);
    return ;
}
int main(){
    int n;
    printf("enter the number ");
    scanf("%d",&n);
    sum(n,0);
    return 0;
}