#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <time.h>
#include <unistd.h>

// Распараллелить алгоритм чет­нечетной перестановки. Показать ускорение. 
// Cделать двумя способами – просто распределять итерации между потоками (при  сравнении   пар),
// и с помощью поблочного распределения массива между потоками и
// чередованием сортировки внутри блока и сравнением­-разделением между потоками. 

#define THREADS 4
#define N 10000
#define GROUPS 100

int group_size = N/GROUPS;
int array[N];

void print_array() {
    for (int i = 0; i < N; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void init_array() {
    for (int i = 0; i < N; i++) {
        array[i] = rand() % 10000;
    }
}

void swap(int i, int j) {
    int x = array[i];
    array[i] = array[j];
    array[j] = x;
}

void sort_pair(int i){
    if (array[i] > array[i+1]) {
        swap(i, i+1);
    }
}

int start(int i) {
    return i;
}

int end(int i) {
    int end = i+group_size;
    if (end >= N) end = N;
    return end;
}

void merge_blocks(int i) {
    int temp[group_size*2];

    int s1 = i*group_size, s2 = (i+1)*group_size;
    int b1 = s1, b2 = s2;
    int t = 0;

    while (b1 < end(s1) && b2 < end(s2)) {
        temp[t++] = array[b1] <= array[b2] ? array[b1++] : array[b2++];
    }

    while (b1 < end(s1)) temp[t++] = array[b1++];
    while (b2 < end(s2)) temp[t++] = array[b2++];
    
    memcpy((void*)(array+start(s1)), temp, t*sizeof(int));
}

void sort1() {
    for (int i = 0; i < N; i++) {

        #pragma omp parallel for
        for (int j = i%2; j < N; j++) {
            sort_pair(j);
        }
    }
}



int cmpfunc (const void * a, const void * b) {return ( *(int*)a - *(int*)b );}

void sort2() {
    #pragma omp parallel for
    for (int i = 0; i < N; i += group_size) {  
        qsort((void*)(array+i), end(i)-start(i), sizeof(int), cmpfunc);
    }
    
    for (int i = 0; i < N; i++) {
        #pragma omp parallel for
        for (int j = i%2; j < GROUPS; j++) {
            merge_blocks(j);
        }
    }
}

int main(){
    omp_set_num_threads(THREADS);
    srand(time(0));

    init_array();
//    print_array(); 

    struct timeval t1, t2;
    double elapsedTime;
    gettimeofday(&t1, NULL);

    sort1();    

    gettimeofday(&t2, NULL);

    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("case 1. data length: %d, threads: %d, time: %gms\n", N, THREADS, elapsedTime);

    init_array();

    gettimeofday(&t1, NULL);

    sort2();    
    
    gettimeofday(&t2, NULL);

    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("case 2. data length: %d, groups: %d, threads: %d, time: %gms\n", N, GROUPS, THREADS, elapsedTime);

    return 0;
}
