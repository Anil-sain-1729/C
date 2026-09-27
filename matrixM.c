#include<stdio.h>
int main(){
    int arr1[3][3];
    int arr2[3][3];
    int arr3[3][3];
    //input for matrix 1
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            scanf("%d",&arr1[i][j]);
        }
        printf("\n");
    }
    //input for matrix 2
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            scanf("%d",&arr2[i][j]);
        }
        printf("\n");
    }
    //print matrix 1
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            printf("%2d",arr1[i][j]);
        }
        printf("\n");
    }
    //print matrix 2
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            printf("%2d",arr2[i][j]);
        }
        printf("\n");
    }
    //intialization final matrix
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            arr3[i][j]=0;
        }
    }
    //multiplication of matrix 1 and matrix 2
    for(int m=0;m<3;m++){
        for(int n=0;n<3;n++){
            for(int k=0;k<3;k++){
                arr3[m][n]+= arr1[m][k]*arr2[k][n];
            }
        }
        printf("\n");
    }
    //output of resultant matrix
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            printf("%2d\t",arr3[i][j]);
        }
        printf("\n");
    }

    return 0;
}