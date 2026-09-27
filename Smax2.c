#include<stdio.h>
#include<limits.h>
int main(){
    int arr[7]={1,5,2,4,7,2,6};
    int max= INT_MIN;
    int smax= INT_MIN;
    for(int i=1;i<7;i++){
        if(max<arr[i]){
            smax = max;
            max = arr[i];
        }
        else if(smax<arr[i]){
            smax = arr[i];
        }
    }
    printf("%d\n",max);
    printf("%d",smax);
}