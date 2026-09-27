#include<stdio.h>
int main(){
   int a[9]= {1,2,3,4,5,6,7,9,8};
    for(int i=0;i<9;i++){
        if(a[0]<a[i]){
            a[0]=a[i];
        }
    }
    printf("%d",a[0]);
   return 0;
}