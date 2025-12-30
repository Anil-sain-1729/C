#include<stdio.h>
int main()
{
    int n;
    printf("enteer the number : ");
    scanf("%d",&n);
    int a=n-1;
    int b=1;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=a;j++){
            printf(" ");
        }
        for(int k=1;k<=b;k++){
            if(i%2==0){
                int c=k+64;
                char ch=(char)c;
                printf("%c",ch);
            }
            else{
                printf("%d",k);
            }
        }
        b+=2;
        a--;
        printf("\n");
    }
    return 0;
}