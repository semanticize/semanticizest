from collections import Sequence
from six.moves import xrange
from six.moves.urllib.parse import quote


def ngrams_with_pos(lst, N=None):
    """Generate n-grams with indices from a list of strings.

    Parameters
    ----------
    lst : list-like of strings
    N : int, optional
        Maximum n-gram length, defaults to the length of `lst`.

    Yields
    -------
    tuple (start, end, n-gram)

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
    if N is None:
        N = len(lst)

    if not isinstance(N, int):
        raise TypeError("n-gram order N should be an integer, was %s" % type(N))

    if N < 1:
        raise ValueError("n-gram order N should be 1 or greater %s" % N)

    join = " ".join

    for start in xrange(len(lst)):
        for n in xrange(1, 1 + min(N, len(lst) - start)):
            yield start, start + n, join(lst[start:start + n])


def ngrams(lst, N=None):
    """Generate bare n-grams from a list of strings.

    See ``ngrams_with_pos``.
    """
    return (ng for _, _, ng in ngrams_with_pos(lst, N))


def tosequence(x):
    """Cast x to sequence. Returns x if at all possible."""
    return x if isinstance(x, Sequence) else list(x)


def url_from_title(title, wiki):
    """Turn an article title into a Wikipedia URL.

    Parameters
    ----------
    wiki : string
        Denotes the specific Wikipedia (language), e.g. "en".

    """
    title = title.strip()
    if not isinstance(title, bytes):
        title = title.encode('utf-8')
    title = title[0].upper() + title[1:]    # Wikipedia-specific
    title = quote(title.replace(' ', '_'), safe=',()/:')
    return "https://{}.wikipedia.org/wiki/{}".format(wiki, title)
