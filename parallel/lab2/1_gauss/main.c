#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <time.h>
#include <unistd.h>

// Реализовать метод Гаусса  для систем произвольной размерности  на   OpenMP.  
// Показать ускорение.

#define THREADS 8
#define N 1024
#define M (N+1)

double matrix[N * M];

void print_matrix() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            printf("%g ", matrix[i * M + j]);
        }
        printf("\n");
    }
    printf("-------------\n");
}

int get_max_elem_row(int column, int start_row) {
    double max_value = fabs(matrix[start_row * M + column]);
    int row_max = start_row;
    for (int row = start_row + 1; row < N;row++) {
        double value = fabs(matrix[row * M + column]);
        if (value > max_value) {
            max_value = value;
            row_max = row;
        }
    }
    return row_max;
}

void divide_row(int row, size_t startIColumn, double divider) {
    for (int i = 0; i < M; i++)
       matrix[row * M + i] /= divider;
}

void row_minus_row(int i, int j, double divider) {
    for (int column = 0; column < M; column++)
        matrix[i * M + column] -= matrix[j * M + column] * divider;
}

void row_swap(int i, int j) {
    for (int k = 0; k < M; k++) {
        double value = matrix[i * M + k];
        matrix[i * M + k] = matrix[j * M + k];
        matrix[j * M + k] = value;
    }
}

void init_matrix() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {            
            matrix[i * M + j] = rand()%1000;
        }
    }
}

void direct(){
    for (int i = 0; i < (M - 1); i++) {
        int row = i;
        int max_elem_row = get_max_elem_row(i, row);
        row_swap(max_elem_row, row);
        divide_row(row, i, matrix[row * M + i]);

        #pragma omp parallel for
        for (int j = row + 1; j < N; ++j) {
            row_minus_row(j, i, matrix[j * M + i]);
        }
    }
}

void reverse(){
    for (int j = M - 2; j >= 0; --j) {
        #pragma omp parallel for
        for (int i = 0; i < j; ++i){
            matrix[i * M + (M - 1)] -= matrix[j * M + (M - 1)] * matrix[i * M + j];
            matrix[i * M + j] = 0;
        }
    }
}

int main(){
    omp_set_num_threads(THREADS);
    srand(time(0));

    init_matrix();
    //print_matrix();

    struct timeval t1, t2;
    double elapsedTime;
    gettimeofday(&t1, NULL);

    direct();
    reverse();
    
    //print_matrix();

    gettimeofday(&t2, NULL);

    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("matrix: %dx%d, threads: %d, time: %gms\n", N, M, THREADS, elapsedTime);

    return 0;
}