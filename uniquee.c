#include<stdio.h>
#include<stdbool.h>
int main(){
   int arr[7]={1,2,5,5,6,2,1};
   for(int i=0;i<7;i++){
       bool number = false;
       for(int j=i+1;j<7;j++){
           if(arr[i]==arr[j]){
              number = true;
           }
       }
       if(number==false){
        printf("%d",arr[i]);
        break;
       }
   }
    return 0;
}