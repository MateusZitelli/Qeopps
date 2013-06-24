int count(int * i){
    mutex_rlock(i);
    while(*i > 3){
        mutex_wlock(i);
        *i = 10;
        mutex_unlock(i);
    }
    mutex_unlock(i);
}
int teste(int * i, int * teste){
    mutex_wlock(teste);
    __transaction_atomic{
        teste = 3;
        while(teste < 5){
            __transaction_atomic{
                teste++;
            }
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
