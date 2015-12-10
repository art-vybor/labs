#include <mpi/mpi.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    
    //split processes
    int size; MPI_Comm_size(MPI_COMM_WORLD, &size);
    int group_size = size / 2;
    int subgroup_ranks[100];
    int subgroup_ranks1[100];

    for (int i = 0, j = 0, k=0; i < group_size * 2; i++) {
        if (i % 2) {   
            subgroup_ranks[j++] = i;
        } else {
            subgroup_ranks1[k++] = i;            
        }
    }
    
    //create two groups
    MPI_Group group; MPI_Comm_group(MPI_COMM_WORLD, &group);
    MPI_Group group1 = MPI_GROUP_NULL; MPI_Group_incl(group, group_size, subgroup_ranks, &group1);
    MPI_Group group2 = MPI_GROUP_NULL; MPI_Group_incl(group, group_size, subgroup_ranks1, &group2);

    //detect current group
    int rank; MPI_Group_rank(group1, &rank);

    char process_in_group = 1;
    if (rank == MPI_UNDEFINED) { //not in group1
        MPI_Group_rank(group2, &rank); 

        process_in_group = 2;
        if (rank == MPI_UNDEFINED) { //not in group 2
            process_in_group = 0;
        }
    }

    if (!process_in_group) {
        MPI_Finalize();
        return 0;
    }

    //find your place in the world    
    int rank1_global = 0; MPI_Group_translate_ranks(group1, 1, &rank, group, &rank1_global);
    int rank2_global = 0; MPI_Group_translate_ranks(group2, 1, &rank, group, &rank2_global);
    

    MPI_Status status;
    
    
    char response[100];

    if (process_in_group == 1) {
        char* request = "ping";        
            
        printf("1.%d sending %s to 2.%d\n", rank1_global, request, rank2_global);

        MPI_Send((void*)request, strlen(request)+1, MPI_CHAR, rank2_global, 0, MPI_COMM_WORLD);

        MPI_Recv((void*)response, 100, MPI_CHAR, rank2_global, 0, MPI_COMM_WORLD, &status);
        // MPI_Sendrecv((void*)request, strlen(request)+1, MPI_CHAR, rank2_global, 0,
        //     (void*)response, strlen(response)+1, MPI_CHAR, rank2_global, 0,
        //     MPI_COMM_WORLD, &status);

        printf("1.%d received %s from 2.%d\n", rank1_global, response, rank2_global);
    } else if (process_in_group == 2){
        char* request = "pong";

        //printf("sending %s: group 2, rank %d -> group 1, rank %d\n", request, rank2_global, rank1_global);

        MPI_Recv((void*)response, 100, MPI_CHAR, rank1_global, 0, MPI_COMM_WORLD, &status);

        printf("2.%d received %s from 1.%d\n", rank2_global, response, rank1_global);

        MPI_Send((void*)request, strlen(request)+1, MPI_CHAR, rank1_global, 0, MPI_COMM_WORLD);
        printf("2.%d sending %s to 1.%d\n", rank2_global, request, rank1_global);        
        // MPI_Sendrecv((void*)request, strlen(request)+1, MPI_CHAR, rank1_global, 0,
        //     (void*)response, strlen(response)+1, MPI_CHAR, rank1_global, 0,
        //     MPI_COMM_WORLD, &status);

        
    }

    MPI_Finalize();

    return 0;
}