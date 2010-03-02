__all__ = ['standard_form']

import numpy as np
import scipy.sparse as sparse

def standard_form(A):
    """Calculate a permutation matrix so that PA is in standard form.

    The column index of the first non-zero element of row i is defined
    as F(i).  When a matrix is in standard form,

      F(i) <= F(i + 1)

    Parameters
    ----------
    A : sparse matrix
        Matrix to be permuted.

    Returns
    -------
    P : sparse matrix
        Permutation matrix such that PA is in standard form.

    Notes
    -----
    The permutation matrix is orthogonal, and as such its
    inverse is simply ``P.T``.

    """
    if not sparse.issparse(A):
        A = sparse.csr_matrix(A)

    A = A.tocsr()
    A.sort_indices()

    # Only examine rows with non-zero elements
    mask = (A.indptr[:-1] < len(A.indices))
    first_col_idx = A.indices[A.indptr[mask]]
    perm = np.argsort(first_col_idx)

    N = A.shape[0]
    L = len(perm)
    ij = np.zeros((2, L))
    ij[0, :] = np.arange(L) + np.sum(~mask)
    ij[1, :] = perm

    return sparse.coo_matrix((np.ones(L), ij), shape=(N, N)).tocsc()
