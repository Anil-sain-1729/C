#include<stdio.h>
int main(){
    int r,c;
    printf("enter the r ");
    scanf("%d",&r);
    printf("enter the c ");
    scanf("%d",&c);
    int arr[r][c];
    for(int i=0;i<r;i++){
        for(int j=0;j<c;j++){
            scanf("%d",&arr[i][j]);
        }
    }
     printf("\n");
    for(int i=0;i<r;i++){
        for(int j=0;j<c;j++){
            if(j%2==0){
                 printf("%3d",arr[i][j]);
            }else{
                printf("%3d",arr[r-1-i][j]);
            }
        }
         printf("\n");
    }
    return 0;
}