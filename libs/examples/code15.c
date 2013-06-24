int count(int * i){
    mutex_rlock(i);
    __transaction_atomic{
        while(*i > 3){
            *i = 10;
        }
    }
    mutex_unlock(i);
}
int teste(int * i, int * teste){
    mutex_wlock(teste);
    teste = 3;
        mutex_rlock(teste);
        __transaction_atomic{
        }
        mutex_unlock(teste);
    while(teste < 5){
        teste++;
    }
    mutex_unlock(teste);
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
