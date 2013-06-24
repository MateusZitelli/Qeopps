int count(int * i){
    __transaction_atomic{
        while(*i > 3){
            __transaction_atomic{
                *i = 10;
            }
        }
    }
}
int teste(int * i, int * teste){
    __transaction_atomic{
        teste = 3;
            __transaction_atomic{
                mutex_wlock(teste);
                mutex_unlock(teste);
            }
        while(teste < 5){
            teste++;
        }
    }
}
int main(void){
    count(i); //defined as int count(int * i)
    while(1){
        teste(a, b); //defined as int teste(int * i, int * teste)
    }
}
