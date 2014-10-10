from cytoolz import compose

from nose.tools import assert_equal

from textwithlinks import clean_text, remove_links
from wikidumps import extract_links, redirect


def test_extract_links():
    first_link = compose(tuple, next, iter, extract_links)

    assert_equal(first_link("[[foo|bar]]"), ("foo", "bar"))
    assert_equal(first_link("[[foo]]"), ("foo", "foo"))
    assert_equal(first_link("[[File:picture!]] [[foo]]"), ("foo", "foo"))
    assert_equal(first_link("[[foo]]bar."), ("foo", "foobar"))
    assert_equal(first_link("[[baz|foobar]];"), ("baz", "foobar"))

    # This construct appears in enwiki for chemical formulae etc., but also in
    # nlwiki (and dewiki?) for more general compound nouns. The current
    # handling may not be exactly what we want; any fix should update the test
    # accordingly.
    assert_equal(list(extract_links("[[Lithium|Li]][[Fluorine|F]]")),
                 [("Lithium", "Li"), ("Fluorine", "F")])
    assert_equal(list(extract_links("[[tera-|tera]][[becquerel]]s")),
                 [("tera-", "tera"), ("becquerel", "becquerels")])


def test_redirect():
    assert_equal(redirect("#ReDiReCt [[frob]] {{R from redirect}}"), "frob")


def test_remove_links():
    text = """
        Wikisyntax is the [[syntax (to be parsed)|syntax]] used on
        [[Wikipedia]].{{citation needed|date=October 2014}}
        We have to parse it, and we use every [[hack]] in the
        [[text]][[book]] that we can find.
    """

    # Note space in "text book", inserted to match extract_links output (see
    # test above). If we don't do this, probabilities won't add up properly.
    expected = """
        Wikisyntax is the syntax used on Wikipedia.
        We have to parse it, and we use every hack in the
        text book that we can find.
    """

    assert_equal(remove_links(clean_text(text)).split(), expected.split())
