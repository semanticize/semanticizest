def ngrams_with_pos(lst not None, N=None):
    """Generate n-grams with indices from a list of strings.

    Parameters
    ----------
    lst : list-like of strings
    N : int, optional
        Maximum n-gram length, defaults to the length of `lst`.

    Returns
    -----
    n_grams : iterable of tuple (start, end, n-gram)
        Tuples are start and end index in the original list `lst`,
        the n-gram is the space joined string value. The n-grams are
        yielded in leftmost longest order.

    Raises
    ------
    TypeError
        If `N` is not an integer.
    ValueError
        If `N` is not at least 1.
    """
    cdef list l

    try:
        l = lst
    except TypeError:
        l = list(lst)

    cdef Py_ssize_t length = len(l)
    cdef Py_ssize_t n = length if N is None else N
    cdef Py_ssize_t i, start

    if n < 1:
        raise ValueError("n-gram order N should be 1 or greater than %d" % N)

    join = " ".join

    return [(start, start + i, join(l[start:start + i]))
            for start in range(length)
            for i in range(1, 1 + min(n, length - start))]
