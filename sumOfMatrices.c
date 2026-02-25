#include<stdio.h>
int main(){
    int a[2][2] = {1,2,3,4};
    for(int i=0;i<2;i++){
        for(int j=0;j<2;j++){
            printf("%2d",a[i][j]);
        }
        printf("\n");
    }
    printf("\n");
    int b[2][2] = {5,6,7,8};
    for(int i=0;i<2;i++){
        for(int j=0;j<2;j++){
            printf("%2d",b[i][j]);
        }
        printf("\n");
    }
    int c[2][2];
    for(int i=0;i<2;i++){
        for(int j=0;j<2;j++){
            c[i][j] = a[i][j]+b[i][j];
        }
    }
    printf("sum of matrices \n");
    for(int i=0;i<2;i++){
        for(int j=0;j<2;j++){
            printf("%3d",c[i][j]);
        }
        printf("\n");
    }    
    return 0;
}