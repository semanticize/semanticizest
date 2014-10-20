from collections import Counter

from semanticizest._util import ngrams, url_from_title

from nose.tools import assert_equal, assert_true


def test_ngrams():
    text = "Hello , world !".split()
    expected = {"Hello , world", ", world !",
                "Hello ,", ", world", "world !",
                "Hello", ",", "world", "!"}

    ng = Counter(ngrams(text, 3))
    assert_equal(set(ng), expected)
    assert_true(all(freq == 1 for freq in ng.values()))


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
