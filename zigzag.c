#include<stdio.h>
void preInPost(int n){
    if(n==0) return;
    printf("%d",n);
    preInPost(n-1);
    printf("%d",n);
    preInPost(n-1);
    printf("%d",n);
    return ;
}
int main(){
    int n;
    printf("enter the number ");
    scanf("%d",&n);
    preInPost(n);
    return 0;
}