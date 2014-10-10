from cytoolz import compose

from nose.tools import assert_equal

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
