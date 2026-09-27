#include<stdio.h>
int main()
{
    int i,j,k,n=5;
    for(i=1;i<=n;i++){
        for(j=1;j<=i;j++){
            for(k=1;k>=n;k--){
                printf(" ");
            }
            printf("%d",i);
        }
        printf("\n");
    }
    return 0;
}