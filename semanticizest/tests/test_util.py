from semanticizest._util import url_from_title

from nose.tools import assert_equal


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
