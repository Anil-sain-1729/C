#include<stdio.h>
int main(){
    int n;
    int sum=1;
    printf("enter the number ");
    scanf("%d",&n);
    int arr[n];
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }
    for(int i=0;i<n;i++){
        printf("%d ",arr[i]);
    }
    for(int i=0;i<n;i++){
    sum *=arr[i];
    }
    printf("\n=%d",sum);
    return 0;
}