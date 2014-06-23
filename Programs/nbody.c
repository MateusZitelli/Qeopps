#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

#define N 1000
#define THREADS_MAX 10


struct vector{



float x;
	float y;
	float z;
}

void init(vector * force, vector * position, vector * speed){



	int i;
	for(i = 0; i < N; i++){
		/*Qeopps-TAG_vect read(force[N]) write(force[N])*/



		force[i].x = 0;
		force[i].y = 0;
		force[i].z = 0;
		speed[i].x = 0;
	speed[i].y = 0;
		speed[i].z = 0;
		position[i].x = rand() % 100000 / 100000 * 1000;
		position[i].y = rand() % 100000 / 100000 * 1000;
		position[i].z = rand() % 100000 / 100000 * 1000;
	}
}

int main(void){
srand(10);
pthread_t threads[THREADS_MAX];
	vector * force, position, speed;
	force = (vector *) malloc(N * sizeof(vector));
	position = (vector *) malloc(N * sizeof(vector));
	speed = (vector *) malloc(N * sizeof(vector));
	init(force, position, speed);
	return 0;
}
