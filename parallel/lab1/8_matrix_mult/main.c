#include <mpi/mpi.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <unistd.h>

// Использовать двумерную  декартову топологию процессов при 
// реализации 
// параллельного перемножения 
// матриц.   Каждый   процесс   считает   элемент  
// результирующей матрицы. 

#define N 5

void print_matrix(int **matrix) {
    
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%d ", matrix[i][j]);
        }
        if (i != N-1) printf("\n");
    }
    printf("\n");
}

struct MATRIX_ELEMENT {
  int i;
  int j;
  int value;
};


int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    
    srand(time(0));

    int rank; MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int size; MPI_Comm_size(MPI_COMM_WORLD, &size);

    //create matrix
    int **matrix = (int**) malloc(sizeof(int*) * N);
    for (int i = 0; i < N; i++)
        matrix[i] = (int*) malloc(sizeof(int) * N);

    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            matrix[i][j] = 1;

    //create data type
    MPI_Datatype MPI_MATRIX_ELEMENT;
    MPI_Datatype types[3] = { MPI_INT, MPI_INT, MPI_INT };
    int block_lengths[3] = { 1, 1, 1 };
    MPI_Aint int_ext; MPI_Type_extent( MPI_INT, &int_ext );
    MPI_Aint offsets[3] = { 0, int_ext, 2*int_ext };
    MPI_Type_struct( 3, block_lengths, offsets, types, &MPI_MATRIX_ELEMENT );
    MPI_Type_commit(&MPI_MATRIX_ELEMENT);

    //create topology
    int dims[2] = {N, N};
    int periods[2] = {0, 0};
    MPI_Comm comm_cart; MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 0, &comm_cart);

    //get coords
    int coords[2];
    MPI_Cart_coords(comm_cart, rank, 2, coords);

    //calculate one element of dest matrix
    int row = coords[0];
    int column = coords[1];

    int result = 0;
    for (int i = 0; i < N; i++) {
        result += matrix[row][i] * matrix[i][column];
    }

    //fill struct
    struct MATRIX_ELEMENT element;
    element.i = coords[0];
    element.j = coords[1];
    element.value = result;

    if (rank != 0) {
        MPI_Send((void*)&element, 1, MPI_MATRIX_ELEMENT, 0, rank, comm_cart);
    } else {
        matrix[0][0] = result;
        for (int i = 1; i < N*N; i++) {
            MPI_Recv((void*)&element, 1, MPI_MATRIX_ELEMENT, i, i, comm_cart, MPI_STATUSES_IGNORE);    
            matrix[element.i][element.j] = element.value;
        }
        print_matrix(matrix);
    }

    //printf("%d, %d, %d\n", coords[0], coords[1], result);
    // MPI_Reduce((void*)array, (void*)recv, array_length, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // MPI_Barrier(MPI_COMM_WORLD);
  
    
    MPI_Finalize();

    return 0;
}
