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

    MPI_Request array_of_requests[1000];
    int array_of_requests_index = 0;

    struct timeval t1, t2;
    double elapsedTime;
    gettimeofday(&t1, NULL);

    for (int i = 0; i < iterations; i++) {
        array_of_requests_index = 0;
        if (rank == 0) {    
            MPI_Isend((void*)&request, 1, MPI_INT, 1, i, MPI_COMM_WORLD, &array_of_requests[array_of_requests_index]);
            array_of_requests_index += 1;
            MPI_Irecv((void*)&response, 1, MPI_INT, 1, i, MPI_COMM_WORLD, &array_of_requests[array_of_requests_index]);
            array_of_requests_index += 1;
        } else {
            MPI_Isend((void*)&request, 1, MPI_INT, 0, i, MPI_COMM_WORLD, &array_of_requests[array_of_requests_index]);
            array_of_requests_index += 1;
            MPI_Irecv((void*)&response, 1, MPI_INT, 0, i, MPI_COMM_WORLD, &array_of_requests[array_of_requests_index]);
            array_of_requests_index += 1;
        }
        MPI_Waitall(array_of_requests_index, array_of_requests, MPI_STATUSES_IGNORE);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    gettimeofday(&t2, NULL);

    
    if (rank == 0) {
        elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
        elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
        printf("time of %d async iterations: %gms\n", iterations, elapsedTime);
    }   
    
    MPI_Finalize();

    return 0;
}
