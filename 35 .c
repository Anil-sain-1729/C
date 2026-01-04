#include<stdio.h>
int main(){
    int maksh[10] = {55,65,24,58,14,25,31,99,45,31};
    for(int i=0;i<10;i++){
        if(maksh[i]<35){
            printf("lessthan 35 student role number %d\n ",i+1);
        }
    }
    return 0;
}