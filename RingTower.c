#include<stdio.h>
void tower(int n, int s, int h, int d){
    if(n==0) return ;
    tower(n-1,s,d,h);
    printf("%c to %c\n",s,d);
    tower(n-1,h,s,d);
    return ;
}
int main(){
    int n;
    printf("enter the number of ring ");
    scanf("%d",&n);
    tower(n,'A','B','c');
    return 0;
}