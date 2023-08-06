#pragma once
#include "numeric/dense.hpp"
#include "numeric/sparse.hpp"

#include "utils/Chrono.hpp"
#include "detail/macros.hpp"

namespace cpb { namespace kpm {

/**
 The KPM scaling factors `a` and `b`
*/
template<class real_t = double>
struct Scale {
    static constexpr auto tolerance = 0.01f; ///< needed because the energy bounds are not precise

    real_t a = 0;
    real_t b = 0;

    Scale() = default;
    Scale(real_t min_energy, real_t max_energy)
        : a(0.5f * (max_energy - min_energy) * (1 + tolerance)),
          b(0.5f * (max_energy + min_energy)) {
        if (std::abs(b / a) < 0.01f * tolerance) {
            b = 0; // rounding to zero saves space in the sparse matrix
        }
    }
    template<class T>
    Scale(Scale<T> const& other) : a(static_cast<T>(other.a)), b(static_cast<T>(other.b)) {}

    explicit operator bool() { return a != 0; }

    /// Apply the scaling factors to a vector
    ArrayX<real_t> operator()(ArrayX<real_t> const& v) const { return (v - b) / a; }
};

/**
 Min and max eigenvalues of the Hamiltonian

 The bounds can be determined automatically using the Lanczos procedure,
 or set manually by the user. Also computes the KPM scaling factors a and b.
*/
template<class scalar_t>
class Bounds {
    using real_t = num::get_real_t<scalar_t>;

    real_t min; ///< the lowest eigenvalue
    real_t max; ///< the highest eigenvalue
    Scale<real_t> factors;

    SparseMatrixX<scalar_t> const* matrix;
    real_t precision_percent;

    int lanczos_loops = 0;  ///< number of iterations needed to converge the Lanczos procedure
    Chrono timer;

public:
    Bounds(SparseMatrixX<scalar_t> const* matrix, real_t precision_percent)
        : matrix(matrix), precision_percent(precision_percent) {}
    /// Set the energy bounds manually, therefore skipping the Lanczos computation
    Bounds(real_t min_energy, real_t max_energy)
        : min(min_energy), max(max_energy), factors(min_energy, max_energy) {}

    /// The KPM scaling factors a and b
    Scale<real_t> scaling_factors() {
        if (!factors) {
            compute_factors();
        }
        return factors;
    }

    /// Return an array with `size` linearly spaced values within the bounds
    ArrayX<real_t> linspaced(idx_t size) const {
        return ArrayX<real_t>::LinSpaced(size, min, max);
    }

    std::string report(bool shortform = false) const;

private:
    /// Compute the scaling factors using the Lanczos procedure
    void compute_factors();
};

CPB_EXTERN_TEMPLATE_CLASS(Bounds)

}} // namespace cpb::kpm
