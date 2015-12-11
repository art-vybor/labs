#include <mpi/mpi.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <unistd.h>

// Сравнить эффективность  реализации  
// функции  
// MPI_SENDRECV  
// с  
// моделированием  той же функциональности при помощи  неблокирующих 
// операций.

int iterations = 1000000;

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    
    //srand(time(0));

    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int request = 2015;
    int response;

    MPI_Status status;

    struct timeval t1, t2;
    double elapsedTime;
    gettimeofday(&t1, NULL);


    for (int i = 0; i < iterations; i++) {

        MPI_Sendrecv((void*)&request, 1, MPI_INT, 1-rank, i, 
            (void*)&response, 1, MPI_INT, 1-rank, i, MPI_COMM_WORLD, &status);
    }
    MPI_Barrier(MPI_COMM_WORLD);

    gettimeofday(&t2, NULL);

    
    if (rank == 0) {
        elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
        elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
        printf("time of %d sendrecv iterations: %gms\n", iterations, elapsedTime);
    }   
    
    MPI_Finalize();

    return 0;
}
