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


def test_redirect():
    assert_equal(redirect("#ReDiReCt [[frob]] {{R from redirect}}"), "frob")
