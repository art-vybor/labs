#include <stdio.h>
#include "mpi.h"


int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int count;
    MPI_Comm_size(MPI_COMM_WORLD, &count);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    printf("MPI_COMM_WORLD: %d\n", rank );

    MPI_Comm reversedCommunicator;
    MPI_Comm_split(MPI_COMM_WORLD, 0, count - rank, &reversedCommunicator);

    MPI_Comm_rank(reversedCommunicator, &rank);
    printf("reversedCommunicator: %d\n", rank );

    MPI_Finalize();

    return 0;
}