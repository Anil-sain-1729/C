#include<stdio.h>
int main(){
    // 1 2
    // 3 4
    // 5 6
    int a[3][2] = {{1,2},{3,4},{5,6,}};
    // 1 2 3 4
    // 5 6 7 8
    int b[2][4] = {{1,2,3,4},{5,6,7,8}};
    int res[3][4];
    //multiptlying
    for(int i=0;i<3;i++){
        for(int j=0;j<4;j++){
            res[i][j] = 0;
            for(int k=0;k<2;k++){ //k=2 use a[][2] andb[2][]
                res[i][j]+=a[i][k]*b[k][j];
            }
        }
    }
    //result
    for(int i=0;i<3;i++){
        for(int j=0;j<4;j++){
            printf("%3d",res[i][j]);
        }
        printf("\n");
    }
    return 0;
}