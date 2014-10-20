#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

#define THREADS_MAX 4 
struct thread_data{
  int thread_id;
  long int * x;
  long int * y;
  long int * z;
};

struct thread_data thread_data_array[THREADS_MAX];

void * init(void *threadarg){
  struct thread_data *args;
  args = (struct thread_data *) threadarg;
  printf("%i\n", args->thread_id);
  while(*args->z < 3e7){
    /*Qeopps-TAG_var read(z,x,y) write(z)*/
    *args->z = *args->z + *args->x + *args->y;
  }
}

int main(void){
  int rc, i;
  long int *z, *x, *y;
  z = (long int *) malloc(sizeof(long int));
  x = (long int *) malloc(sizeof(long int));
  y = (long int *) malloc(sizeof(long int));
  *z = 0;
  *x = 5;
  *y = 10;
  pthread_t threads[THREADS_MAX];
  for(i = 0; i < THREADS_MAX; i++){
    thread_data_array[i].thread_id = i;
    thread_data_array[i].x = x;
    thread_data_array[i].y = y;
    thread_data_array[i].z = z;
    rc = pthread_create(&threads[i], NULL, init, (void *) &thread_data_array[i]);
  }
  pthread_exit(NULL);
  return 0;
}
