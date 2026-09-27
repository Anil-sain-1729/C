#include<stdio.h>
int main(){
    int sum1=0;
    int sum2=55;
    int arr[9]={1,2,3,5,6,7,8,9,10};
    for(int i=0;i<9;i++){
        sum1+=arr[i];
    }
    printf("missing number %d",sum2-sum1);
}