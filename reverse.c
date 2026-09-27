#include<stdio.h>
void reverse(int arr[]){
    int i=0,j=7;
    while(i<j){
        int tabe = arr[i];
        arr[i]=arr[j];
        arr[j]=tabe;
        i++;
        j--;
    }
    return ;
}
int main(){
    int arr[8]={1,5,2,4,7,7,2,6};
    reverse(arr);
    for(int i=0;i<8;i++){
        printf("%d,",arr[i]);
    }
}