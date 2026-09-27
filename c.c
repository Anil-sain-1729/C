// // // // #include<stdio.h>
// // // // int main(){
// // // //     int arr[5] = {5,4,3,2,1};
// // // //     int n=5;
// // // //     for(int i=0;i<n;i++){
// // // //         printf("print the unsorted array %d ",arr[i]);
// // // //     }
// // // //     // bobble sort 
// // // //     for(int i=0;i<n-1;i++){
// // // //         for(int j=0;j<n-i;j++){  // j<n-i  iski jagh per ham j<n-1 ka bhi use kar sakte hai par loop time lega
// // // //             if(arr[j]>arr[j+1]){
// // // //                 int temp = arr[j];
// // // //                 arr[j] = arr[j+1];
// // // //                 arr[j+1] = temp;
// // // //             }
// // // //         }
// // // //     }
// // // //     printf("\n");
// // // //     for(int i=0;i<n;i++){
// // // //         printf("print the sorted array %d ",arr[i]);
// // // //     }
// // // //     return 0;
// // // // }

// // // // // out put
// // // // // 5 4 3 2 1 
// // // // // 1 2 3 4 5


// // // #include<stdio.h>
// // // int main(){
// // //     int arr[5] = {1,2,3,4,5};
// // //     int n=5;
// // //     for(int i=0;i<n;i++){
// // //         printf("print the unsorted array %d ",arr[i]);
// // //     }
// // //     // bobble sort 
// // //     for(int i=0;i<n-1;i++){
// // //         for(int j=0;j<n-i;j++){  // j<n-i  iski jagh per ham j<n-1 ka bhi use kar sakte hai par loop time lega
// // //             if(arr[j]<arr[j+1]){
// // //                 int temp = arr[j];
// // //                 arr[j] = arr[j+1];
// // //                 arr[j+1] = temp;
// // //             }
// // //         }
// // //     }
// // //     printf("\n");
// // //     for(int i=0;i<n;i++){
// // //         printf("print the sorted array %d ",arr[i]);
// // //     }
// // //     return 0;
// // // }

// // // // out put
// // // // 5 4 3 2 1 
// // // // 1 2 3 4 5


// // #include<stdio.h>
// // #include<limits.h>
// // int main(){
// //     int arr[7] = {7,8,9,5,3,6,1};
// //     int n = 7;
// //     printf("Unsorted array :\n ");
// //     for(int i=0;i<n;i++){
// //         printf(" %d",arr[i]);
// //     }
// //     // selection sort
// //     for(int i=0;i<n-1;i++){
// //         int min = INT_MAX;
// //         int minidx = -1;
// //         for(int j=1;j<n-1;j++){
// //             if(min>arr[j]){
// //                 min = arr[j];
// //                 minidx = j;
// //             }
// //         }
// //         //swap the min amd first element of unsorted part
// //         // swap minidx ani i
// //         int temp = arr[minidx];
// //         arr[minidx] = arr[i];
// //         arr[i] = temp; 
// //     }
// //     printf("\n");
// //     printf("Sorted array : \n");
// //     for(int i=0;i<n;i++){
// //         printf(" %d",arr[i]);

// //     }
// //     return 0;
// // }

// // // out put
// // // Unsorted array :
// // //  7 8 9 5 3 6 1
// // // Sorted array :
// // //  3 9 8 7 6 5 1

// #include<stdio.h>
// #defind MAX_SIZE 100
// int main(){
//     int arr[MAX_SIZE];
//     int i,size,num,pos;
//     printf("enter size of array :");
//     scanf("%d",&size);
//     printf("enter elements of the array :");
//     for(int i=0;i<size;i++){
//         scanf("%d",&arr[i]);
//     }
//     printf("enter elemint")
// }



 