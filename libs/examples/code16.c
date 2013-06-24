int count(int * i){
    mutex_rlock(i);
    mutex_wlock(i);
    while(*i > 3){
        *i = 10;
    }
    mutex_unlock(i);
    mutex_unlock(i);
}
int teste(int * i, int * teste){
    __transaction_atomic{
        mutex_wlock(teste);
        teste = 3;
        while(teste < 5){
            mutex_rlock(teste);
            teste++;
            mutex_unlock(teste);
        }
        mutex_unlock(teste);
    }
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
