#include<stdio.h>
int main()
{
    int arr[3]={10,70,30};
    int max=arr[0];
    for(int i=1;i<=3;i++){
        if (arr[i]>max){
            max=arr[i];
        }
    }
    printf("max valu= %d\n",max);
    return 0;
}