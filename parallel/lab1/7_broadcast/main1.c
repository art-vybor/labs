#include <mpi/mpi.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <unistd.h>

//  Смоделировать глобальное 
// суммирование методом сдваивания и 
// сравнить эффективность такой реализации 
// с функцией MPI_Reduce.

#define array_length  10000

int array[array_length];

int print_array(int* array, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);    
    
    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int size; MPI_Comm_size(MPI_COMM_WORLD, &size);

    srand(clock()*(rank+1));

    for (int i = 0; i < array_length; i++) {
        array[i] = rand() % 10;
    }

    struct timeval t1, t2;
    double elapsedTime;
    gettimeofday(&t1, NULL);

    if (rank == 0) { //final
        for (int i = 1; i < size; i++) {
            MPI_Send((void*)array, array_length, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
    } else { //send
        MPI_Recv((void*)array, array_length, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
    }


    MPI_Barrier(MPI_COMM_WORLD);

    gettimeofday(&t2, NULL);

    
    
    if (rank == 0) {
        // print_array(request, array_length);
        elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
        elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
        printf("time of manual bcast: %gms\n", elapsedTime);
    }   
    
    MPI_Finalize();

    return 0;
}
