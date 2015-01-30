from collections import Sequence

from six.moves.urllib.parse import quote

from ._fast_ngrams import ngrams_with_pos


def ngrams(lst, N=None):
    """Generate bare n-grams from a list of strings.

    See Also
    --------
    ngrams_with_pos : iterable of string

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
