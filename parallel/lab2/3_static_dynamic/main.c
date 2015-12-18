#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
//#include <unistd.h>

// Придумать пример (можно  искусственный), в котором динамическое 
// планирование итераций имело бы 
// преимущество в производительности над 
// статической.

#define THREADS 16
#define ITERATIONS 10000
#define ITERATIONS_IN_BLOCK 100
int main(){
    omp_set_num_threads(THREADS);
    srand(time(0));

    struct timeval t1, t2, sleep_time;
    double elapsedTime;
    sleep_time.tv_sec = 0;
    sleep_time.tv_usec = 10;

    
    gettimeofday(&t1, NULL);
    #pragma omp parallel for schedule (static, ITERATIONS_IN_BLOCK)
    for (int i = 0; i < ITERATIONS; i++) nanosleep(&sleep_time, NULL);
    gettimeofday(&t2, NULL);
    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("static: %gms\n", elapsedTime);

    gettimeofday(&t1, NULL);
    #pragma omp parallel for schedule (dynamic, ITERATIONS_IN_BLOCK)
    for (int i = 0; i < ITERATIONS; i++) nanosleep(&sleep_time, NULL);
    gettimeofday(&t2, NULL);
    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("dynamic: %gms\n", elapsedTime);

    return 0;
}