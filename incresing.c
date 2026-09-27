#include<stdio.h>
void in(int x, int n){
    if(x>n) return;
    printf("%d\n",x);
    in(x+1,n);
    return ;
}
int main(){
    int n;
    printf("enter the nummber ");
    scanf("%d",&n);
    in(1,n);
    return 0;
}