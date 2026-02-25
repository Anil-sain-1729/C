#include<stdio.h>
int main(){
    int arr[7]={1,5,2,4,7,2,6};
    int odd=0,even=0,x;
    for(int i=0;i<7;i++){
        if(i%2!=0){
            odd+=arr[i];
        }else{
            even+=arr[i];
        }
        x=-even+odd;
    }
    printf("%d",x);
}