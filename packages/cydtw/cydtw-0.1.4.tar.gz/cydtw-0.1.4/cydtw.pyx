import numpy
from scipy.spatial.distance import cdist

cimport numpy
DTYPE = numpy.float
ctypedef numpy.float_t DTYPE_t
# "def" can type its arguments but not have a return type. The type of the
# arguments for a "def" function is checked at run-time when entering the
# function.
cimport cython

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def dtw_path(numpy.ndarray[DTYPE_t, ndim=2] s1, numpy.ndarray[DTYPE_t, ndim=2] s2):
    """dtw_path(s1, s2)
    Compute DTW similarity measure between (possibly multidimensional) time series and return the path and the similarity.
    Time series must be 2d numpy arrays of shape (size, dim). It is not required that both time series share the same
    length, but they must be the same dimension. dtype of the arrays must be numpy.float."""
    assert s1.dtype == DTYPE and s2.dtype == DTYPE
    # The "cdef" keyword is also used within functions to type variables. It
    # can only be used at the top indentation level (there are non-trivial
    # problems with allowing them in other places, though we'd love to see
    # good and thought out proposals for it).
    cdef int l1 = s1.shape[0]
    cdef int l2 = s2.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int argmin_pred = -1
    cdef numpy.ndarray[DTYPE_t, ndim=2] cross_dist = cdist(s1, s2, "sqeuclidean").astype(DTYPE)
    cdef numpy.ndarray[DTYPE_t, ndim=2] cum_sum = numpy.zeros((l1 + 1, l2 + 1), dtype=DTYPE)
    cum_sum[1:, 0] = numpy.inf
    cum_sum[0, 1:] = numpy.inf
    cdef numpy.ndarray[numpy.int_t, ndim=3] predecessors = numpy.zeros((l1, l2, 2), dtype=numpy.int) - 1
    cdef numpy.ndarray[DTYPE_t, ndim=1] candidates = numpy.zeros((3, ), dtype=DTYPE)
    cdef list best_path

    for i in range(l1):
        for j in range(l2):
            candidates[0] = cum_sum[i, j + 1]
            candidates[1] = cum_sum[i + 1, j]
            candidates[2] = cum_sum[i, j]
            if candidates[0] <= candidates[1] and candidates[0] <= candidates[2]:
                argmin_pred = 0
            elif candidates[1] <= candidates[2]:
                argmin_pred = 1
            else:
                argmin_pred = 2
            cum_sum[i + 1, j + 1] = candidates[argmin_pred] + cross_dist[i, j]
            if i + j > 0:
                if argmin_pred == 0:
                    predecessors[i, j, 0] = i - 1
                    predecessors[i, j, 1] = j
                elif argmin_pred == 1:
                    predecessors[i, j, 0] = i
                    predecessors[i, j, 1] = j - 1
                else:
                    predecessors[i, j, 0] = i - 1
                    predecessors[i, j, 1] = j - 1

    i = l1 - 1
    j = l2 - 1
    best_path = [(i, j)]
    while predecessors[i, j, 0] >= 0 and predecessors[i, j, 1] >= 0:
        i, j = predecessors[i, j, 0], predecessors[i, j, 1]
        best_path.insert(0, (i, j))

    return best_path, numpy.sqrt(cum_sum[l1, l2])

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def dtw(numpy.ndarray[DTYPE_t, ndim=2] s1, numpy.ndarray[DTYPE_t, ndim=2] s2):
    """dtw(s1, s2)
    Compute DTW similarity measure between (possibly multidimensional) time series and return the similarity.
    Time series must be 2d numpy arrays of shape (size, dim). It is not required that both time series share the same
    length, but they must be the same dimension. dtype of the arrays must be numpy.float."""
    assert s1.dtype == DTYPE and s2.dtype == DTYPE
    # The "cdef" keyword is also used within functions to type variables. It
    # can only be used at the top indentation level (there are non-trivial
    # problems with allowing them in other places, though we'd love to see
    # good and thought out proposals for it).
    cdef int l1 = s1.shape[0]
    cdef int l2 = s2.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef numpy.ndarray[DTYPE_t, ndim=2] cross_dist = cdist(s1, s2, "sqeuclidean").astype(DTYPE)
    cdef numpy.ndarray[DTYPE_t, ndim=2] cum_sum = numpy.zeros((l1 + 1, l2 + 1), dtype=DTYPE)
    cum_sum[1:, 0] = numpy.inf
    cum_sum[0, 1:] = numpy.inf

    for i in range(l1):
        for j in range(l2):
            cum_sum[i + 1, j + 1] = min(cum_sum[i, j + 1], cum_sum[i + 1, j], cum_sum[i, j]) + cross_dist[i, j]

    return numpy.sqrt(cum_sum[l1, l2])