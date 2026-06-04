// Fixed-data BLIS reproducer for the faulty step:
//
//     C = (V * S) @ V.T
//
// where V is 100x10, S is length 10, and (V * S) denotes scaling each
// column of V by S[j].  The data files are plain ASCII:
//
//     rows cols
//     value_00 value_01 ...
//     ...
//
// This program has no parser dependency; it only needs CBLAS for dgemm.

#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Minimal CBLAS declarations to avoid depending on a packaged cblas.h header.
// Values follow the standard Netlib CBLAS ABI used by BLIS/OpenBLAS/Accelerate.
enum CBLAS_ORDER { CblasRowMajor = 101, CblasColMajor = 102 };
enum CBLAS_TRANSPOSE { CblasNoTrans = 111, CblasTrans = 112, CblasConjTrans = 113 };
void cblas_dgemm(
    const enum CBLAS_ORDER Order,
    const enum CBLAS_TRANSPOSE TransA,
    const enum CBLAS_TRANSPOSE TransB,
    const int M,
    const int N,
    const int K,
    const double alpha,
    const double *A,
    const int lda,
    const double *B,
    const int ldb,
    const double beta,
    double *C,
    const int ldc
);

static double *read_matrix(const char *path, int *rows, int *cols) {
    FILE *f = fopen(path, "r");
    if (f == NULL) {
        fprintf(stderr, "Cannot open %s: %s\n", path, strerror(errno));
        exit(2);
    }
    if (fscanf(f, "%d %d", rows, cols) != 2 || *rows <= 0 || *cols <= 0) {
        fprintf(stderr, "Invalid header in %s\n", path);
        exit(2);
    }
    size_t n = (size_t)(*rows) * (size_t)(*cols);
    double *data = (double *)malloc(n * sizeof(double));
    if (data == NULL) {
        fprintf(stderr, "Out of memory reading %s\n", path);
        exit(2);
    }
    for (size_t i = 0; i < n; ++i) {
        if (fscanf(f, "%lf", &data[i]) != 1) {
            fprintf(stderr, "Expected %zu values in %s, stopped at %zu\n", n, path, i);
            exit(2);
        }
    }
    fclose(f);
    return data;
}

int main(int argc, char **argv) {
    const char *fixture_dir = argc > 1 ? argv[1] : "blis_eigsh_reproducer/fixtures";
    char v_path[4096];
    char s_path[4096];
    snprintf(v_path, sizeof(v_path), "%s/V_100_10.txt", fixture_dir);
    snprintf(s_path, sizeof(s_path), "%s/S_100_10.txt", fixture_dir);

    int rows_v, cols_v, rows_s, cols_s;
    double *V = read_matrix(v_path, &rows_v, &cols_v);
    double *S = read_matrix(s_path, &rows_s, &cols_s);
    if (rows_v != 100 || cols_v != 10 || rows_s != 10 || cols_s != 1) {
        fprintf(
            stderr,
            "Unexpected shapes: V=%dx%d S=%dx%d (expected V=100x10 S=10x1)\n",
            rows_v, cols_v, rows_s, cols_s
        );
        return 2;
    }

    const int n = rows_v;
    const int rank = cols_v;
    double *VS = (double *)malloc((size_t)n * rank * sizeof(double));
    double *C_blas = (double *)calloc((size_t)n * n, sizeof(double));
    double *C_ref = (double *)malloc((size_t)n * n * sizeof(double));
    if (VS == NULL || C_blas == NULL || C_ref == NULL) {
        fprintf(stderr, "Out of memory\n");
        return 2;
    }

    // VS = V @ diag(S), implemented as direct column scaling to keep the
    // reproducer focused on the faulty final dgemm.
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < rank; ++j) {
            VS[(size_t)i * rank + j] = V[(size_t)i * rank + j] * S[j];
        }
    }

    // Faulty step on BLIS macOS arm64:
    //     C_blas = VS @ V.T
    cblas_dgemm(
        CblasRowMajor,
        CblasNoTrans,
        CblasTrans,
        n,
        n,
        rank,
        1.0,
        VS,
        rank,
        V,
        rank,
        0.0,
        C_blas,
        n
    );
    // Non-BLAS reference for B=V.T without materializing it.
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double acc = 0.0;
            for (int p = 0; p < rank; ++p) {
                acc += VS[(size_t)i * rank + p] * V[(size_t)j * rank + p];
            }
            C_ref[(size_t)i * n + j] = acc;
        }
    }

    double max_abs = 0.0;
    double max_ref = 0.0;
    double max_out = 0.0;
    int finite = 1;
    for (int i = 0; i < n * n; ++i) {
        double err = fabs(C_blas[i] - C_ref[i]);
        if (err > max_abs) max_abs = err;
        double ar = fabs(C_ref[i]);
        if (ar > max_ref) max_ref = ar;
        double ao = fabs(C_blas[i]);
        if (ao > max_out) max_out = ao;
        if (!isfinite(C_blas[i])) finite = 0;
    }
    double rel = max_abs / (max_ref == 0.0 ? 1.0 : max_ref);
    int bad = rel > 1e-9 || !finite;
    printf(
        "C dgemm fixed-data V*S@V.T: max_abs_err=%.17e rel_err=%.17e max|out|=%.17e%s\n",
        max_abs,
        rel,
        max_out,
        bad ? "   <<< MISMATCH (bug reproduced)" : "   (ok)"
    );

    free(V);
    free(S);
    free(VS);
    free(C_blas);
    free(C_ref);
    return bad ? 1 : 0;
}
