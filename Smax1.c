#include<stdio.h>
#include<limits.h>
int main(){
    int arr[7]={1,5,2,4,7,2,6};
    int max= INT_MIN;
    int smax= INT_MIN;
    for(int i=1;i<7;i++){
        if(max<arr[i]){
            max=arr[i];
        }
    }
    for(int i=1;i<7;i++){
        if(arr[i]!=max && smax<arr[i]){
           smax=arr[i];
        }
    }
    printf("%d",smax);
}