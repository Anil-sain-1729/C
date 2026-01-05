#include<stdio.h>
int main(){
    int n;
    printf("enter the number n ");
    scanf("%d",&n);
    int m;
    printf("enter the number m ");
    scanf("%d",&m);
    int arr[n][m];
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            scanf("%d",&arr[i][j]);
        }
    }
    printf("\n");
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            printf("%3d",arr[i][j]);
        }
        printf("\n");
    }
    //spiral print
    printf("\n");
    int minr = 0;
    int maxr = n-1;
    int minc = 0;
    int maxc = m-1;
    int tner = n*m;
    int count = 0;
    while(count<tner){
        // print the minimue row
        for(int j=minc;j<=maxc;j++){
            printf("% d",arr[minr][j]);
            count++;
        }
        minr++;
        //print the maxiume colume 
        for(int i=minr;i<=maxr;i++){
            printf("% d",arr[i][maxc]);
            count++;
        }
        maxc--;
        // print the maxiume row
        for(int j=maxc;j>=minc;j--){
            printf("% d",arr[maxr][j]);
            count++;
        }
        maxr--;
        // print the minimue colume
        for(int i=maxr;i>=minr;i--){
            printf("% d",arr[i][minc]);
            count++;
        }
        minc++;
    }
    return 0;
}