import re
import sqlite3
from os.path import join, dirname, abspath

from nose.tools import assert_equal

import semanticizest.parse_wikidump
from semanticizest import Semanticizer
from semanticizest._wiki_dump_parser import parse_dump

#ugh...
db = sqlite3.connect(':memory:')
cur = db.cursor()
with open(join(dirname(semanticizest.parse_wikidump.__file__),
               "createtables.sql")) as create:
    cur.executescript(create.read())
dump = join(dirname(abspath(__file__)),
            'nlwiki-20140927-pages-articles-sample.xml')
parse_dump(dump, db, N=2)
link_count = {(t, a): c for
              t, a, c in cur.execute('select target, ngram as anchor, count '
                                     'from linkstats, ngrams '
                                     'where ngram_id = ngrams.id;')}
sem = Semanticizer(link_count, N=2)


def test_semanticizer():
    # raise SkipTest()
    # here = os.path.dirname(os.path.abspath(__file__))
    # dump = os.path.join(here, 'nlwiki-20140927-pages-articles-sample.xml')

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
