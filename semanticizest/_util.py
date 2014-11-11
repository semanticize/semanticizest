from collections import Sequence
from six.moves import xrange
from six.moves.urllib.parse import quote

from ._ngrams import ngrams, ngrams_with_pos    # re-export


def tosequence(x):
    """Cast x to sequence. Returns x if at all possible."""
    return x if isinstance(x, Sequence) else list(x)


def url_from_title(title, wiki):
    """Turn article title into Wikipedia URL.

    wiki denotes the specific Wikipedia (language), e.g. "en".
    """
    title = title.strip()
    if not isinstance(title, bytes):
        title = title.encode('utf-8')
    title = title[0].upper() + title[1:]    # Wikipedia-specific
    title = quote(title.replace(' ', '_'), safe=',()/:')
    return "https://{}.wikipedia.org/wiki/{}".format(wiki, title)
