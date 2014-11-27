import re
from os.path import join, dirname

from nose.tools import assert_equal

from semanticizest import Semanticizer
from semanticizest._semanticizer import create_model


# create in-memory db
db = create_model(join(dirname(__file__),
                       'nlwiki-20140927-pages-articles-sample.xml'), 'nlwiki_test.sqlite3')
sem = Semanticizer('nlwiki_test.sqlite3', N=2)


def test_semanticizer():
    text = """Aangezien de aarde een planeet is, kunnen de aardwetenschappen
ook als een tak van de planetologie beschouwd worden. Aardwetenschappelijke
kennis, met name geomorfologie, wordt bijvoorbeeld ook toegepast voor de
zoektocht naar sporen van water, sneeuw en ijs op de planeet Mars."""
    tokens = re.split(r'\W+', text)

    expected = set(['Planeet', 'Planetologie', 'Kennis (wetenschap)',
                    'Geomorfologie', 'Mars (planeet)'])
    concepts = set(string for _, _, string, _ in sem.all_candidates(tokens))

    assert_equal(expected, concepts)


def test_semanticizer_redirect():
    text = """In 1902 werkte hij even bij een Architekt."""
    tokens = re.split(r'\W+', text)

    expected = set(['Architect'])
    actual = set(string for _, _, string, _ in sem.all_candidates(tokens))

    assert_equal(expected, actual)
