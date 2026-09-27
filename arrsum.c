#include<stdio.h>
int main()
{
    int n,i,sum=0;
    printf("enter tne number of elements: ");
    scanf("%d",&n);
    int arr[n];
    printf("enter the number of the arr: \n");
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }for(i=0;i<n;i++){
        sum += arr[i];
    }
    printf("sum of the arr elements = %d\n",sum);
    return 0;
}