int count(int * i){
    __transaction_atomic{
        mutex_wlock(i);
        while(*i > 3){
            *i = 10;
        }
        mutex_unlock(i);
    }
}
int teste(int * i, int * teste){
    __transaction_atomic{
        teste = 3;
        while(teste < 5){
            __transaction_atomic{
                __transaction_atomic{
                    teste++;
                }
            }
        }
    }
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
