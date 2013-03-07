#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t mutex_data = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t new_data_condition = PTHREAD_COND_INITIALIZER, redy_condition = PTHREAD_COND_INITIALIZER;

void * modify(void * arg){
  int * data = (int *) arg;
  int val = 0, i, j;
  while(val < 1000){
    pthread_mutex_lock(&mutex_data);
    *data = val;
    pthread_mutex_unlock(&mutex_data);
    pthread_cond_signal(&new_data_condition);
    val += 1;
    j = 0;
    for(i = 10E4; i > val; i--)
      j += i;
    printf("TESTETESTE\n");
  }
}

void * print(void * arg){
  int * data = (int *) arg;
  int i, j;
  while(1){
    #pragma omp
    pthread_mutex_lock(&mutex_data);
    pthread_cond_wait(&new_data_condition, &mutex_data);
    printf("%i\n", * data);
    pthread_mutex_unlock(&mutex_data);
    j = 0;
    for(i = 10E4; i > 0; i--)
      j += i;
  }
}

extern int main(void){
  pthread_t thread_io, thread_execute;
  int data;
  pthread_create(&thread_io, NULL, &modify, &data);
  pthread_create(&thread_execute, NULL, &print, &data);
  pthread_join(thread_io, NULL);
}
