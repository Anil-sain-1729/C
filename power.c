#include<stdio.h>
int power(int a , int b){
    if(b==0) return 1;
    return a*power(a,b-1);
}
int main(){
    int a,b;
    printf("enter the valu : ");
    scanf("%d %d",&a,&b);
    int p=power(a,b);
    printf(" %d",p);
    return 0;
}