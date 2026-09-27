#include<stdio.h>
void fun(int x[]){
    int tabe = x[0];
    x[0]=x[1];
    x[1]=tabe;
    return ;
}
int main(){
    int arr[2]={2,9};
    printf("%d  %d\n",arr[0],arr[1]);
    fun(arr);
    printf("%d  %d\n",arr[0],arr[1]);
}