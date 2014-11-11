cimport cython


cdef object join = " ".join


@cython.boundscheck(False)
@cython.wraparound(False)
def ngrams_with_pos(list lst not None, unsigned N):
    """Generate n-grams for 1 <= n <= N from lst."""

    cdef Py_ssize_t start, end, n, length = len(lst)

    for start in range(length):
        for n in range(1, 1 + min(N, length - start)):
            yield start, start + n, join(lst[start:start + n])


@cython.boundscheck(False)
@cython.wraparound(False)
def ngrams(list lst not None, unsigned N):
    cdef Py_ssize_t start, end, n, length = len(lst)

    for start in range(length):
        for n in range(1, 1 + min(N, length - start)):
            yield join(lst[start:start + n])
