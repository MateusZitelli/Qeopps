int count(int * i){
    __transaction_atomic{
        while(*i > 3){
            mutex_wlock(i);
            *i = 10;
            mutex_unlock(i);
        }
    }
}
int teste(int * i, int * teste){
    __transaction_atomic{
        teste = 3;
            __transaction_atomic{
            }
        while(teste < 5){
            mutex_wlock(teste);
            teste++;
            mutex_unlock(teste);
        }
    }
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}