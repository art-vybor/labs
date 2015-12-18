#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

// Придумать пример (можно  искусственный), в котором множество 
// потоков 
// имеют доступ к разделяемому 
// ресурсу через критическую секцию. 

#define THREADS 16
#define ITERATIONS 10000

int main(){
    omp_set_num_threads(THREADS);
    srand(time(0));

    struct timeval t1, t2, sleep_time;
    double elapsedTime;
    sleep_time.tv_sec = 0;
    sleep_time.tv_usec = 10;

    
    gettimeofday(&t1, NULL);

    int sum = 0;

    #pragma omp parallel for
    for (int i = 0; i < ITERATIONS; i++) {
        sleep_time.tv_sec = 0;
        sleep_time.tv_usec = rand()%1000000;
        nanosleep(&sleep_time, NULL);

        #pragma omp critical 
        sum += 1;
    }
    printf("sum: %d, expected: %d\n", sum, ITERATIONS);

    gettimeofday(&t2, NULL);
    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("time: %gms\n", elapsedTime);

    return 0;
}