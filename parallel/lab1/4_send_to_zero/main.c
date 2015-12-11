#include <mpi/mpi.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

// Переслать нулевому 
// процессу от всех процессов приложения  структуру 
// (структуру создать на уровне 
// MPI), состоящую из ранга процесса и 
// названия узла, на котором данный процесс 
// запущен (полученного с помощью 
// MPI_GET_PROCESSOR_NAME). 

struct NODE_INFO {
  int rank;
  char hostname[MPI_MAX_PROCESSOR_NAME+1];
};

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    struct NODE_INFO node_info;

    int size; MPI_Comm_size(MPI_COMM_WORLD, &size);
    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    node_info.rank = rank;    
    int hostname_length;
    MPI_Get_processor_name(node_info.hostname, &hostname_length);
    //node_info.hostname[hostname_length] = 0;

    MPI_Datatype MPI_NODE_INFO;
    MPI_Datatype types[2] = { MPI_INT, MPI_CHAR };
    int block_lengths[2] = { 1, hostname_length+1 };
    MPI_Aint int_ext; MPI_Type_extent( MPI_INT, &int_ext );
    MPI_Aint offsets[2] = { 0, int_ext };
    MPI_Type_struct( 2, block_lengths, offsets, types, &MPI_NODE_INFO );
    MPI_Type_commit(&MPI_NODE_INFO);

    if (rank != 0) {
        MPI_Send((void*)&node_info, 1, MPI_NODE_INFO, 0, 0, MPI_COMM_WORLD);
    } else {
        MPI_Status status;
        struct NODE_INFO info;
        
        for (int i = 1; i < size; ++i) {
            MPI_Recv((void*)&info, 1, MPI_NODE_INFO, i, 0, MPI_COMM_WORLD, &status);
            printf("%s - %d\n", info.hostname, info.rank);
        }
    }

    MPI_Finalize();

    return 0;
}