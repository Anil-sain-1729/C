#include<stdio.h>
#include<string.h>
int main(){
    char str[100];
    puts("enter a string : \n");
    scanf("%[^\n]s",str);
    // size
    int size = 0;
    int k = 0;
    while(str[k]!='\0'){
        size++;
        k++;
    }
    for(int i=0,j=size-1;i<=j;i++,j--){
        char temp = str[i];
        str[i] = str[i];
        str[j] = temp;
    }
    printf("the reverse string is : \n");
    puts(str);
    return 0;
}