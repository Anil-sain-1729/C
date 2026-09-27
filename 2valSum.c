#include<stdio.h>
int main(){
    int x=9,totel=0;
    int arr[7]={1,5,2,4,7,2,6};
   for(int i=0;i<7;i++){
      for(int j=i+1;j<7;j++){
        if(arr[i]+arr[j]==x){
           totel++;
        printf("(%d , %d)\n",arr[i],arr[j]);
        }
      }
   }
   printf("%d\n",totel);
}