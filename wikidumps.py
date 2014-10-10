"""Parsing utilities for Wikipedia database dumps."""

from __future__ import print_function

from collections import Counter
from itertools import chain
import re
import xml.etree.ElementTree as etree   # don't use LXML, it's slower (!)

from semanticizest._util import ngrams


def _get_namespace(tag):
    try:
        namespace = re.match(r"^{(.*?)}", tag).group(1)
    except AttributeError:
        namespace = ''
    if not namespace.startswith("http://www.mediawiki.org/xml/export-"):
        raise ValueError("namespace %r not recognized as MediaWiki dump"
                         % namespace)
    return namespace


def extract_pages(f):
    """Extract pages from Wikimedia database dump.

    Parameters
    ----------
    f : file-like or str
        Handle on Wikimedia article dump. May be any type supported by
        etree.iterparse.

    Returns
    -------
    pages : iterable over (int, string, string)
        Generates (page_id, title, content) triples.
        In Python 2.x, may produce either str or unicode strings.
    """
    elems = (elem for _, elem in etree.iterparse(f, events=["end"]))

    # We can't rely on the namespace for database dumps, since it's changed
    # it every time a small modification to the format is made. So, determine
    # those from the first element we find, which will be part of the metadata,
    # and construct element paths.
    elem = next(elems)
    namespace = _get_namespace(elem.tag)
    ns_mapping = {"ns": namespace}
    ns_path = "./{%(ns)s}ns" % ns_mapping
    page_tag = "{%(ns)s}page" % ns_mapping
    text_path = "./{%(ns)s}revision/{%(ns)s}text" % ns_mapping
    id_path = "./{%(ns)s}id" % ns_mapping
    title_path = "./{%(ns)s}title" % ns_mapping

    for elem in elems:
        if elem.tag == page_tag:
            if elem.find(ns_path).text != '0':
                continue

            text = elem.find(text_path).text
            if text is None:
                # Empty article; these occur in Wikinews dumps.
                continue
            yield (int(elem.find(id_path).text),
                   elem.find(title_path).text,
                   text)

            # Prune the element tree, as per
            # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
            # We do this only for <page>s, since we need to inspect the
            # ./revision/text element. That shouldn't matter since the pages
            # comprise the bulk of the file.
            elem.clear()


def extract_links(article):
    """Extract all (or most) links from article text (wiki syntax).

    Returns an iterable over (target, anchor) pairs.
    """
    links = re.findall(r"\[\[ ([^]]+) \]\] (\w*)", article, re.VERBOSE)

    for l, extra in links:
        if '|' in l:
            target, anchor = l.split('|', 1)
        else:
            target, anchor = l, l
        # If the anchor contains a colon, assume it's a file or category link.
        if ':' in target:
            continue

        anchor += extra
        yield target, anchor


def redirect(page):
    """Return redirect target for page, if any, else None."""
    m = re.match(r"\#REDIRECT \s* \[\[ ([^]]+) \]\]", page,
                 re.IGNORECASE | re.VERBOSE)
    return m and m.group(1)


_UNWANTED = re.compile(r"""
  (:?
    # we must catch nested {{}} and {| |}; allow one level of nesting
    \{ [|{] (?: \{ [|{] .*? [|}] \} | .*? )* [|}] \}
  | <math> .*? </math>
  | <ref .*? > .*? </ref>
  | \[\[ [^][:]* : (\[\[.*?\]\]|.)*? \]\]   # media, categories
  | =+ .*? =+                               # headers
  | ''+
  )
""", re.DOTALL | re.MULTILINE | re.VERBOSE)


def clean_text(page):
    """Return the clean-ish running text parts of a page."""
    return re.sub(_UNWANTED, "", page)


_LINK_SYNTAX = re.compile(r"""
    (?:
        \[\[
        (?: [^]|]* \|)?     # "target|" in [[target|anchor]]
    |
        \]\]
    )
""", re.DOTALL | re.MULTILINE | re.VERBOSE)


def remove_links(page):
    """Remove links from clean_text output."""
    page = re.sub(r'\]\]\[\[', ' ', page)       # hack hack hack, see test
    return re.sub(_LINK_SYNTAX, '', page)


def page_statistics(page, N=7, sentence_splitter=None, tokenizer=None):
    """Gather statistics from a single WP page.

    The sentence_splitter should be a callable that splits text into sentences.
    It defaults to an unspecified heuristic.

    Returns
    -------
    stats : (dict, dict)
        The first dict maps (target, anchor) pairs to counts.
        The second maps n-grams (up to N) to counts.
    """
    clean = clean_text(page)
    link_counts = Counter(extract_links(clean))

    no_links = remove_links(clean)
    if sentence_splitter is None:
        sentences = re.split(r'(?:\n{2,}|\.\s+)', no_links, re.MULTILINE)
    else:
        sentences = [sentence for paragraph in re.split('\n+', no_links)
                              for sentence in paragraph]

    if tokenizer is None:
        tokenizer = str.split
    ngram_counts = Counter(chain.from_iterable(ngrams(tokenizer(sentence), N)
                                               for sentence in sentences))

    return link_counts, ngram_counts


if __name__ == "__main__":
    # Test; will write article info + prefix of content to stdout
    import sys

    if len(sys.argv) > 1:
        print("usage: %s; will read from standard input" % sys.argv[0],
              file=sys.stderr)
        sys.exit(1)

    for pageid, title, text in extract_pages(sys.stdin):
        title = title.encode("utf-8")
        print(title)
        for target, anchor in extract_links(text):
            print("    %s -> %s"
                  % (anchor.encode("utf-8"), target.encode("utf-8")))
