int count(int * i){
    __transaction_atomic{
        __transaction_atomic{
            while(*i > 3){
                *i = 10;
            }
        }
    }
}
int teste(int * i, int * teste){
    mutex_wlock(teste);
    teste = 3;
        mutex_rlock(teste);
        mutex_wlock(teste);
        mutex_unlock(teste);
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
