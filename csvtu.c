#include<stdio.h>
int main()
{ 
  int i,j;
  for(int i=1;i<=7;i++){
    //c
    for(int j=1;j<=7;j++){
      if(i==1||j==1||i==7){
        printf("*");
      }else{
        printf(" ");
      }
    }
    for(int j=1;j<=4;j++){
      printf(" ");
    }
    //s
    for(int j=1;j<=7;j++){
      if(i==1||i==4||i==7||i<=3&&j==1||i>=5&&j==7){
        printf("*");
      }else{
        printf(" ");
      }
    }
    for(int j=1;j<=4;j++){
      printf(" ");
    }
    //v
    for(int j=1;j<=7;j++){
      if(i<=4&&j==1||i<=4&&j==7||i==5&&j==2||i==5&&j==6||i==6&&j==3||i==6&&j==5||i==7&&j==4){
        printf("*");
      }else{
        printf(" ");
      }
    }
    for(int j=1;j<=4;j++){
      printf(" ");
    }
    //t
    for(int j=1;j<=7;j++){
      if(i==1||j==4){
        printf("*");
      }else{
        printf(" ");
      }
    }
    for(int j=1;j<=4;j++){
      printf(" ");
    }
    //u
    for(int j=1;j<=7;j++){
      if(i==7||j==1||j==7){
        printf("*");
      }else{
        printf(" ");
      }
    }
    printf("\n");
  }
  return 0;
} 