from six.moves.urllib.parse import quote


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
