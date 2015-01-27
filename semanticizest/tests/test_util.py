from collections import Counter

from semanticizest._util import ngrams, ngrams_with_pos, url_from_title

from nose.tools import assert_equal, assert_in, assert_true, raises


def test_ngrams():
    text = "Hello , world !".split()
    expected = {"Hello , world", ", world !",
                "Hello ,", ", world", "world !",
                "Hello", ",", "world", "!"}

    ng = Counter(ngrams(text, 3))
    assert_equal(set(ng), expected)
    assert_true(all(freq == 1 for freq in ng.values()))

    with_pos = list(ngrams_with_pos(text, 2))
    assert_in((0, 2, 'Hello ,'), with_pos)
    assert_in((1, 3, ', world'), with_pos)


@raises(ValueError)
def test_ngrams_order_0():
    lst = "a b c".split()
    # The execution of the generator is delayed until the values are
    # requested, so that's the first opportunity at which an Exception
    # can/will be raised.
    list(ngrams_with_pos(lst, -3))


def test_ngrams_order_1():
    lst = "a b c".split()
    actual = list(ngrams(lst, 1))
    expected = lst
    assert_equal(expected, actual)


def test_ngrams_order_2():
    lst = "a b c".split()
    actual = list(ngrams(lst, 2))
    expected = ["a", "a b",
                "b", "b c",
                "c"]
    assert_equal(expected, actual)


def test_ngrams_order_3():
    lst = "a b c".split()
    actual = list(ngrams(lst, 3))
    expected = ["a", "a b", "a b c",
                "b", "b c",
                "c"]
    assert_equal(expected, actual)


def test_ngrams_order_4():
    # same result as test_ngrams_order_3...
    lst = "a b c".split()
    actual = list(ngrams(lst, 4))
    expected = ["a", "a b", "a b c",
                "b", "b c",
                "c"]
    assert_equal(expected, actual)


def test_ngrams_order_none():
    # same result as test_ngrams_order_3...
    lst = "a b c".split()
    actual = list(ngrams(lst, None))
    expected = ["a", "a b", "a b c",
                "b", "b c",
                "c"]
    assert_equal(expected, actual)


@raises(TypeError)
def test_ngrams_order_string():
    # This has bitten me three(!) times now. Basta!
    lst = "a b c".split()
    list(ngrams_with_pos(lst, 'foobar'))


def test_url_from_title():
    """Test article title -> Wikipedia URL conversion."""
    assert_equal(url_from_title('L. R. Ford, Jr.', 'en'),
                 'https://en.wikipedia.org/wiki/L._R._Ford,_Jr.')
    assert_equal(url_from_title('Graph (mathematics)', 'en'),
                 'https://en.wikipedia.org/wiki/Graph_(mathematics)')
    assert_equal(url_from_title('z/OS', 'en'),
                 'https://en.wikipedia.org/wiki/Z/OS')
    assert_equal(url_from_title('ZOS: Zone of Separation', 'en'),
                 'https://en.wikipedia.org/wiki/ZOS:_Zone_of_Separation')
    assert_equal(url_from_title('Iezergeteri-je', 'nds-nl'),
                 'https://nds-nl.wikipedia.org/wiki/Iezergeteri-je')
    assert_equal(url_from_title(u'Zw\xe4rte W\xe4ter', 'nds-nl'),
                 'https://nds-nl.wikipedia.org/wiki/Zw%C3%A4rte_W%C3%A4ter')
