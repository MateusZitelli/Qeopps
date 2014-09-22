#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

#define N 500
#define THREADS_MAX 10
struct thread_data{
  int thread_id;
  struct vector * force;
  struct vector * position;
  struct vector * speed;
};

struct vector{
  float x;
	float y;
	float z;
};

struct thread_data thread_data_array[THREADS_MAX];

void * init(void *threadarg){
	int i, j;
  struct thread_data *args;
  args = (struct thread_data *) threadarg;
	for(j = 0; j < 100; j++){
		for(i = 0; i < N; i++){
			/*Qeopps-TAG_vect read(force[N]) write(force[N])*/
			/*Qeopps-TAG_vect read(speed[N]) write(speed[N])*/
			/*Qeopps-TAG_vect read(position[N]) write(position[N])*/
			args->force[i].x = 0;
			args->force[i].y = 0;
			args->force[i].z = 0;
			args->speed[i].x = 0;
			args->speed[i].y = 0;
			args->speed[i].z = 0;
			args->position[i].x = rand() % 100000 / 100000 * 1000;
			args->position[i].y = rand() % 100000 / 100000 * 1000;
			args->position[i].z = rand() % 100000 / 100000 * 1000;
		}
	}
}

int main(void){
  int rc, i;
  srand(10);
  pthread_t threads[THREADS_MAX];
	struct vector * force, * position, * speed;
	force = (struct vector *) malloc(N * sizeof(struct vector));
	position = (struct vector *) malloc(N * sizeof(struct vector));
	speed = (struct vector *) malloc(N * sizeof(struct vector));
  for(i = 0; i < THREADS_MAX; i++){
    thread_data_array[i].thread_id = i;
    thread_data_array[i].force = force;
    thread_data_array[i].position = position;
    thread_data_array[i].speed = speed;
    rc = pthread_create(&threads[i], NULL, init, (void *) &thread_data_array[i]);
  }
  pthread_exit(NULL);
  return 0;
}
