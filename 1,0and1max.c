#include<stdio.h>
int main(){
   int arr[3][4]= {{1,0,1,1},{0,1,0,1,},{1,1,1,1}};
   // 1 0 1 1 
   // 0 1 0 1
   // 1 0 0 1 
   int maxCount = 0,maxInd=-1;
    for(int i=0;i<3;i++){
        int count = 1;
        for(int j=0;j<3;j++){
            if(arr[i][j]==1) count++;
        }
        if(maxCount < count){
            maxCount = count;
            maxInd = i;
        }
    }
    printf("%d\n%d",maxCount,maxInd);
   return 0;
}