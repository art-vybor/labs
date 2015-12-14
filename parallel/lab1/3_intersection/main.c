#include <mpi/mpi.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

// Разбить все процессы 
// приложения на три произвольных группы и   напечатать  
// ранги в MPI_COMM_WORLD тех  процессов, что попали в первые две 
// группы, но не попали в третью. 

int* get_random_ranks_array(int subgroup_size) {
    int size; MPI_Comm_size(MPI_COMM_WORLD, &size);

    int *subgroup_ranks = malloc(subgroup_size);

    int ranks[100];
    for (int i = 0; i < size; i++) ranks[i] = i;

    for (int i = 0; i < subgroup_size; i++) {
        int random_key = rand() % size;
        subgroup_ranks[i] = ranks[random_key];

        ranks[random_key] = ranks[size-1];
        size--;
    }

    return subgroup_ranks;
}

int print_group(int* group, int size, char* text) {
    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    char s[1000]; 
    char *ptr = s;
    ptr[0] = 0;
    for (int i = 0; i < size; i++) {
        int n = sprintf(ptr, "%d ", group[i]);
        ptr += n;
    }

    printf("%d.%s: [%s]\n", rank, text, s);
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    //set seed
    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    srand(time(0)*(rank+1));

    if (rank == 1) {
        //generate 3 groups
        int size; MPI_Comm_size(MPI_COMM_WORLD, &size);

        int subgroup1_size = rand() % size;
        int *subgroup1_ranks = get_random_ranks_array(subgroup1_size);

        int subgroup2_size = rand() % size;
        int *subgroup2_ranks = get_random_ranks_array(subgroup2_size);

        int subgroup3_size = rand() % size;
        int *subgroup3_ranks= get_random_ranks_array(subgroup3_size);

        MPI_Group group; MPI_Comm_group(MPI_COMM_WORLD, &group);
        MPI_Group subgroup1 = MPI_GROUP_NULL; MPI_Group_incl(group, subgroup1_size, subgroup1_ranks, &subgroup1);
        MPI_Group subgroup2 = MPI_GROUP_NULL; MPI_Group_incl(group, subgroup2_size, subgroup2_ranks, &subgroup2);
        MPI_Group subgroup3 = MPI_GROUP_NULL; MPI_Group_incl(group, subgroup3_size, subgroup3_ranks, &subgroup3);


        //intersect
        MPI_Group intersected, result;
        MPI_Group_intersection(subgroup1, subgroup2, &intersected);
        MPI_Group_difference(intersected, subgroup3, &result);

        int result_size; MPI_Group_size(result, &result_size);
        int result_ranks[100];

        for (int i = 0; i < result_size; i++) result_ranks[i] = i;
            

        int rank_result[100]; MPI_Group_translate_ranks(result, result_size, &result_ranks, group, rank_result);
    
        print_group(subgroup1_ranks, subgroup1_size, "1");
        print_group(subgroup2_ranks, subgroup2_size, "2");
        print_group(subgroup3_ranks, subgroup3_size, "3");

        print_group(rank_result, result_size, "result");   
    }



    MPI_Finalize();

    return 0;
}