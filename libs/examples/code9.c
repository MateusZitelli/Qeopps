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
    mutex_wlock(teste);
    __transaction_atomic{
        teste = 3;
            mutex_rlock(teste);
            mutex_unlock(teste);
        while(teste < 5){
            teste++;
        }
    }
    mutex_unlock(teste);
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
