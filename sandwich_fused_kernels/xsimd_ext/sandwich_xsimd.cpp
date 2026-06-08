// Fused sandwich product X.T @ diag(d) @ X using xsimd + OpenMP.
// Mirrors tabmat's block-outer strategy with explicit SIMD batches.

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <vector>

#include <xsimd/xsimd.hpp>

#ifdef _OPENMP
#include <omp.h>
#endif

namespace {

using batch = xsimd::batch<double>;
constexpr std::size_t kBatch = batch::size;
constexpr int kBlock = 4;

inline void rank1_update_block(
    double* acc,
    int ld,
    const double* x_row,
    int i0,
    int j0,
    int ni,
    int nj,
    double w
) {
    for (int li = 0; li < ni; ++li) {
        const double xi = x_row[i0 + li] * w;
        int lj = 0;
        for (; lj + static_cast<int>(kBatch) <= nj; lj += static_cast<int>(kBatch)) {
            batch xj = xsimd::load_unaligned(x_row + j0 + lj);
            batch a = xsimd::load_unaligned(acc + li * ld + lj);
            a += xi * xj;
            xsimd::store_unaligned(acc + li * ld + lj, a);
        }
        for (; lj < nj; ++lj) {
            acc[li * ld + lj] += xi * x_row[j0 + lj];
        }
    }
}

inline void flush_block_acc(
    double* out,
    int m,
    const double* acc,
    int ld,
    int i0,
    int j0,
    int ni,
    int nj,
    bool diagonal_block
) {
    for (int li = 0; li < ni; ++li) {
        for (int lj = 0; lj < nj; ++lj) {
            const int gi = i0 + li;
            const int gj = j0 + lj;
            const double v = acc[li * ld + lj];
            if (diagonal_block) {
                if (gi > gj) {
                    continue;
                }
                out[gi * m + gj] += v;
                if (gi != gj) {
                    out[gj * m + gi] += v;
                }
            } else {
                out[gi * m + gj] += v;
                out[gj * m + gi] += v;
            }
        }
    }
}

inline void accumulate_tabmat_blocks(
    const double* X,
    const double* d,
    double* out,
    int n_rows,
    int n_cols,
    int block
) {
    const int n_blocks = (n_cols + block - 1) / block;
    for (int jb = 0; jb < n_blocks; ++jb) {
        const int j0 = jb * block;
        const int j1 = std::min(j0 + block, n_cols);
        const int nj = j1 - j0;
        for (int ib = 0; ib <= jb; ++ib) {
            const int i0 = ib * block;
            const int i1 = std::min(i0 + block, n_cols);
            const int ni = i1 - i0;
            double acc[kBlock * kBlock] = {0.0};
            for (int k = 0; k < n_rows; ++k) {
                const double w = d[k];
                const double* x_row = X + static_cast<std::size_t>(k) * n_cols;
                rank1_update_block(acc, block, x_row, i0, j0, ni, nj, w);
            }
            flush_block_acc(out, n_cols, acc, block, i0, j0, ni, nj, ib == jb);
        }
    }
}

void sandwich_xsimd_impl(
    const double* X,
    const double* d,
    double* out,
    int n_rows,
    int n_cols,
    int n_threads
) {
    std::memset(out, 0, static_cast<std::size_t>(n_cols) * n_cols * sizeof(double));

#ifdef _OPENMP
    if (n_threads > 0) {
        omp_set_num_threads(n_threads);
    }
    if (n_threads > 1) {
        const int n_chunks = std::max(n_threads * 4, 1);
        const int k_chunk = (n_rows + n_chunks - 1) / n_chunks;
        const int actual_chunks = (n_rows + k_chunk - 1) / k_chunk;
        const std::size_t block_elems =
            static_cast<std::size_t>(n_cols) * static_cast<std::size_t>(n_cols);
        const std::size_t partial_elems = block_elems * static_cast<std::size_t>(actual_chunks);
        std::vector<double> partial(partial_elems, 0.0);

#pragma omp parallel for num_threads(n_threads) schedule(static)
        for (int cb = 0; cb < actual_chunks; ++cb) {
            const int k0 = cb * k_chunk;
            const int k1 = std::min(k0 + k_chunk, n_rows);
            const double* Xc = X + static_cast<std::size_t>(k0) * n_cols;
            const double* dc = d + k0;
            double* part = partial.data() + static_cast<std::size_t>(cb) * block_elems;
            accumulate_tabmat_blocks(Xc, dc, part, k1 - k0, n_cols, kBlock);
        }

        for (int cb = 0; cb < actual_chunks; ++cb) {
            const double* part = partial.data() + static_cast<std::size_t>(cb) * block_elems;
            for (std::size_t i = 0; i < block_elems; ++i) {
                out[i] += part[i];
            }
        }
        return;
    }
#endif
    accumulate_tabmat_blocks(X, d, out, n_rows, n_cols, kBlock);
}

}  // namespace

extern "C" {

void sandwich_xsimd_f64(
    const double* X,
    const double* d,
    double* out,
    std::int64_t n_rows,
    std::int64_t n_cols,
    int n_threads
) {
    sandwich_xsimd_impl(
        X,
        d,
        out,
        static_cast<int>(n_rows),
        static_cast<int>(n_cols),
        n_threads
    );
}

std::int64_t sandwich_xsimd_batch_width() {
    return static_cast<std::int64_t>(kBatch);
}

}  // extern "C"
