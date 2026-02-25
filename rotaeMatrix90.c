#include<stdio.h>
int main(){
   int n;
   printf("enter the n  ");
   scanf("%d",&n);
   int a[n][n];
   //input
   for(int i=0;i<n;i++){
       for(int j=0;j<n;j++){
           scanf("%d",&a[i][j]);
       }
   }
   //transpose
   for(int i=0;i<n;i++){
      for(int j=0;j<i;j++){
         int temp = a[i][j];
         a[i][j] = a[j][i];
         a[j][i] = temp;
      }
   }
   //rotate
   for(int i=0;i<n;i++){
      int j=0,k=n-1;
      while(j<k){
          int temp = a[i][j];
          a[i][j] = a[i][k];
          a[i][k] = temp;
          j++;
          k--;
      }
   }
   printf("\n");
   // output
   for(int i=0;i<n;i++){
       for(int j=0;j<n;j++){
           printf("%2d",a[i][j]);
       }
       printf("\n");
   }
   return 0;
}