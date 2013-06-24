#include <stdio.h>         
         int count(int * i){
    /*Queopps-TAG read(i) write()*/
    while(*i > 3){
        /*Queopps-TAG read() write(i)*/
  *i = 10;
}
}

int teste(int * i, int * teste){
    /*Queopps-TAG read() write(teste)*/
    teste = 3;
             while(teste < 500){
     /*Queopps-TAG read(teste) write(teste)*/
        teste++;
             }
}
    


       int main(void){
        int a, b,i;
         for(i=0; i < 100000; i++){
  count(i);
        teste(a, b);
          }
}

