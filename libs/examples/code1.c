int count(int * i){
    mutex_rlock(i);
    while(*i > 3){
        __transaction_atomic{
            *i = 10;
        }
    }
    mutex_unlock(i);
}
int teste(int * i, int * teste){
    __transaction_atomic{
        mutex_rlock(teste);
        mutex_wlock(teste);
        teste = 3;
        while(teste < 5){
            teste++;
        }
        mutex_unlock(teste);
        mutex_unlock(teste);
    }
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
