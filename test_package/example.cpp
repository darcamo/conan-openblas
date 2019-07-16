#include <cblas.h>
#include <cstdlib>
#include <stdio.h>

/* Parameters */
#define M 6
#define N 5
#define LDA M
#define LDU M
#define LDVT N

// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// xxxxxxxxxxxxxxx Prototypes xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
void run_cblas_dgemm();
// void run_svd();
extern void dgesvd(char *jobu, char *jobvt, int *m, int *n, double *a, int *lda,
                   double *s, double *u, int *ldu, double *vt, int *ldvt,
                   double *work, int *lwork, int *info);
extern void print_matrix(char *desc, int m, int n, double *a, int lda);


// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// xxxxxxxxxxxxxxx Helper functions xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

void run_cblas_dgemm() {
  int i = 0;
  double A[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
  double B[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
  double C[9] = {.5, .5, .5, .5, .5, .5, .5, .5, .5};
  cblas_dgemm(CblasColMajor, CblasNoTrans, CblasTrans, 3, 3, 2, 1, A, 3, B, 3,
              2, C, 3);

  for (i = 0; i < 9; i++)
    printf("%lf ", C[i]);
  printf("\n");
}

// void run_svd() {
//  /* Locals */
//         int m = M, n = N, lda = LDA, ldu = LDU, ldvt = LDVT, info, lwork;
//         double wkopt;
//         double* work;
//         /* Local arrays */
//         double s[N], u[LDU*M], vt[LDVT*N];
//         double a[LDA*N] = {
//             8.79,  6.11, -9.15,  9.57, -3.49,  9.84,
//             9.93,  6.91, -7.93,  1.64,  4.02,  0.15,
//             9.83,  5.04,  4.86,  8.83,  9.80, -8.99,
//             5.45, -0.27,  4.85,  0.74, 10.00, -6.02,
//             3.16,  7.98,  3.01,  5.80,  4.27, -5.31
//         };
//         /* Executable statements */
//         printf( " DGESVD Example Program Results\n" );
//         /* Query and allocate the optimal workspace */
//         lwork = -1;
//         dgesvd( "All", "All", &m, &n, a, &lda, s, u, &ldu, vt, &ldvt, &wkopt, &lwork,
//          &info );
//         lwork = (int)wkopt;
//         work = (double*)malloc( lwork*sizeof(double) );
//         /* Compute SVD */
//         dgesvd( "All", "All", &m, &n, a, &lda, s, u, &ldu, vt, &ldvt, work, &lwork,
//          &info );
//         /* Check for convergence */
//         if( info > 0 ) {
//                 printf( "The algorithm computing SVD failed to converge.\n" );
//                 exit( 1 );
//         }
//         /* Print singular values */
//         print_matrix( "Singular values", 1, n, s, 1 );
//         /* Print left singular vectors */
//         print_matrix( "Left singular vectors (stored columnwise)", m, n, u, ldu );
//         /* Print right singular vectors */
//         print_matrix( "Right singular vectors (stored rowwise)", n, n, vt, ldvt );
//         /* Free workspace */
//         free( (void*)work );
// }

/* Auxiliary routine: printing a matrix */
void print_matrix(char *desc, int m, int n, double *a, int lda) {
  int i, j;
  printf("\n %s\n", desc);
  for (i = 0; i < m; i++) {
    for (j = 0; j < n; j++)
      printf(" %6.2f", a[i + j * lda]);
    printf("\n");
  }
}

int main(int argc, char *argv[]) {
    run_cblas_dgemm();
  return 0;
}
