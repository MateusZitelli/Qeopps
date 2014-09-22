         int count(int * i){
    /*Qeopps-TAG read(i) write()*/
    while(*i > 3){
        /*Qeopps-TAG read() write(i)*/
  *i = 10;
}
}

int teste(int * i, int * teste){
    /*Qeopps-TAG read() write(teste)*/
    teste = 3;
             while(teste < 100000){
     /*Qeopps-TAG read(teste) write(teste)*/
        teste++;
             }
}
    


       int main(void){
        int a,b,i;
  count(&i);
         for(i=0; i < 10000; i++){
        teste(&a, &b);
          }
}

