#include <stdio.h>
#include <pthread.h>
#define NUM_THREADS 10
pthread_mutex_t mutex_read_threadid = PTHREAD_MUTEX_INITIALIZER;
void *PrintHello(void *threadid){
    pthread_mutex_lock(&mutex_read_threadid);
    int i;
    for(i = 0; i++ ; i < 200000){
        threadid+=10;
    }
    long tid;
    tid = (long)threadid;
    printf("Hello World! It's me, thread #%ld!\n", tid);
    pthread_mutex_unlock(&mutex_read_threadid);
}
int main(void){
    int rc;
    long t;
    void *status;
    pthread_t threads[NUM_THREADS];
    for(t=0; t<NUM_THREADS; t++){
        rc = pthread_create(&threads[t], NULL, PrintHello, (void *)t);
    }
    for(t=0; t < NUM_THREADS; t++){
        pthread_join(threads[t], &status);
    }
    return 0;
}
