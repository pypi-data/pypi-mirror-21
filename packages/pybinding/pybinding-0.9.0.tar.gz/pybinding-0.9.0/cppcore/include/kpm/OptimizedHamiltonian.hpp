#pragma once
#include "kpm/Bounds.hpp"
#include "kpm/Config.hpp"

#include "numeric/sparse.hpp"
#include "numeric/ellmatrix.hpp"

#include "support/variant.hpp"
#include "utils/Chrono.hpp"
#include "detail/macros.hpp"

namespace cpb { namespace kpm {

/**
 Indices of the Green's function matrix that will be computed

 A single KPM calculation will compute an entire `row` of the Green's matrix,
 however only some column indices are required to be saved, as indicated by `cols`.
 */
struct Indices {
    storage_idx_t row = -1;
    ArrayXi cols;

    Indices() = default;
    Indices(idx_t row, idx_t col) : row(static_cast<storage_idx_t>(row)), cols(1) {
        cols[0] = static_cast<storage_idx_t>(col);
    }
    Indices(idx_t row, std::vector<idx_t> const& cols)
        : row(static_cast<storage_idx_t>(row)),
          cols(eigen_cast<ArrayX>(cols).cast<storage_idx_t>()) {}
    Indices(idx_t row, ArrayXi cols)
        : row(static_cast<storage_idx_t>(row)), cols(std::move(cols)) {}

    /// Indicates a single element on the main diagonal
    bool is_diagonal() const { return cols.size() == 1 && row == cols[0]; }

    friend bool operator==(Indices const& l, Indices const& r) {
        return l.row == r.row && all_of(l.cols == r.cols);
    }
};

/**
 Optimized slice mapping for `optimal_size` and `interleaved` KPM algorithms.
 */
class SliceMap {
    std::vector<storage_idx_t> data; ///< optimized Hamiltonian indices marking slice borders
    idx_t offset = 0; ///< needed to correctly compute off-diagonal elements (i != j)

public:
    /// Simple constructor for non-optimized case -> single slice equal to full system size
    explicit SliceMap(idx_t system_size) { data = {static_cast<storage_idx_t>(system_size)}; }
    /// Map for optimized matrix. The `optimized_idx` is needed to compute the `offset`
    SliceMap(std::vector<storage_idx_t> border_indices, Indices const& optimized_idx);

    /// Return an index into `data`, indicating the optimal system size for
    /// the calculation of KPM moment number `n` out of total `num_moments`
    idx_t index(idx_t n, idx_t num_moments) const {
        assert(n < num_moments);

        auto const max = std::min(last_index(), num_moments / 2);
        if (n < max) {
            return n; // size grows in the beginning
        } else { // constant in the middle and shrinking near the end as reverse `n`
            return std::min(max, num_moments - 1 - n + offset);
        }
    }

    /// Last index into `data`
    idx_t last_index() const { return static_cast<idx_t>(data.size()) - 1; }

    /// Return the optimal system size for KPM moment number `n` out of total `num_moments`
    idx_t optimal_size(idx_t n, idx_t num_moments) const {
        return data[index(n, num_moments)];
    }

    /// Would calculating this number of moments ever do a full matrix-vector multiplication?
    bool uses_full_system(idx_t num_moments) const {
        return static_cast<idx_t>(data.size()) < num_moments / 2;
    }

    idx_t operator[](idx_t i) const { return data[i]; }
    std::vector<storage_idx_t> const& get_data() const { return data; }
    idx_t get_offset() const { return offset; }
};

/**
 Stores a scaled Hamiltonian `(H - b)/a` which limits it to (-1, 1) boundaries required for KPM.
 In addition, three optimisations are applied (last two are optional, see `MatrixConfig`):

 1) The matrix is multiplied by 2. This benefits most calculations (e.g. `y = 2*H*x - y`),
    because the 2x multiplication is done only once, but it will need to be divided by 2
    when the original element values are needed (very rarely).

 2) Reorder the elements so that target indices are placed at the start of the matrix.
    This produces a `SliceMap` which may be used to reduce calculation time by skipping
    sparse matrix-vector multiplication of zero values or by interleaving calculations
    of neighboring slices.

 3) Convert the sparse matrix into the ELLPACK format. The sparse matrix-vector
    multiplication algorithm for this format is much easier to vectorize compared
    to the classic CSR format.
 */
template<class scalar_t>
class OptimizedHamiltonian {
    using real_t = num::get_real_t<scalar_t>;
    using OptMatrix = var::variant<SparseMatrixX<scalar_t>, num::EllMatrix<scalar_t>>;

    OptMatrix optimized_matrix; ///< reordered for faster compute
    Indices optimized_idx; ///< reordered target indices in the optimized matrix
    SliceMap slice_map; ///< slice border indices
    std::vector<storage_idx_t> reorder_map; ///< mapping from original matrix indices to reordered indices

    SparseMatrixX<scalar_t> const* original_matrix;
    Indices original_idx; ///< original target indices for which the optimization was done

    MatrixFormat matrix_format;
    bool is_reordered;
    Chrono timer;

public:
    OptimizedHamiltonian(SparseMatrixX<scalar_t> const* m, MatrixFormat const& mf, bool reorder)
        : slice_map(m->rows()), original_matrix(m), matrix_format(mf), is_reordered(reorder) {}

    /// Create the optimized Hamiltonian targeting specific indices and scale factors
    void optimize_for(Indices const& idx, Scale<real_t> scale);

    /// Apply new Hamiltonian index ordering to a container
    template<class Vector>
    void reorder(Vector& v) const {
        if (reorder_map.empty()) { return; }
        assert(reorder_map.size() == static_cast<size_t>(v.size()));

        auto reordered_v = Vector(v.size());
        for (auto i = idx_t{0}; i < reordered_v.size(); ++i) {
            reordered_v[reorder_map[i]] = v[i];
        }
        v.swap(reordered_v);
    }

    void reorder(SparseMatrixX<scalar_t>& matrix) const;

    idx_t size() const { return original_matrix->rows(); }
    Indices const& idx() const { return optimized_idx; }
    SliceMap const& map() const { return slice_map; }
    OptMatrix const& matrix() const { return optimized_matrix; }

private:
    /// Just scale the Hamiltonian: H2 = (H - I*b) * (2/a)
    void create_scaled(Indices const& idx, Scale<real_t> scale);
    /// Scale and reorder the Hamiltonian so that idx is at the start of the optimized matrix
    void create_reordered(Indices const& idx, Scale<real_t> scale);
    /// Convert CSR matrix into ELLPACK format
    static num::EllMatrix<scalar_t> convert_to_ellpack(SparseMatrixX<scalar_t> const& csr);
    /// Get optimized indices which map to the given originals
    static Indices reorder_indices(Indices const& original_idx,
                                   std::vector<storage_idx_t> const& reorder_map);

    /// Total non-zeros processed when computing `num_moments` with or without size optimizations
    size_t num_nonzeros(idx_t num_moments, bool optimal_size) const;
    /// Same as above but with vector elements instead of sparse matrix non-zeros
    size_t num_vec_elements(idx_t num_moments, bool optimal_size) const;
    /// The amount of memory (in bytes) used by the Hamiltonian matrix
    size_t matrix_memory() const;
    /// Memory used by a single KPM vector
    size_t vector_memory() const;

    friend struct Stats;
};

CPB_EXTERN_TEMPLATE_CLASS(OptimizedHamiltonian)

}} // namespace cpb::kpm
