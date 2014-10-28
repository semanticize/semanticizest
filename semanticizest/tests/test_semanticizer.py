import os.path
import re

from nose.tools import assert_less_equal
from semanticizest import Semanticizer
from semanticizest._wiki_dump_parser import parse_dump


def test_semanticizer():
    here = os.path.dirname(os.path.abspath(__file__))
    dump = os.path.join(here, 'nlwiki-20140927-pages-articles-sample.xml')
    link_count, ngram_count = parse_dump(dump, N=2)
    sem = Semanticizer(link_count)

    text = """Aangezien de aarde een planeet is, kunnen de aardwetenschappen
ook als een tak van de planetologie beschouwd worden. Aardwetenschappelijke
kennis, met name geomorfologie, wordt bijvoorbeeld ook toegepast voor de
zoektocht naar sporen van water, sneeuw en ijs op de planeet Mars."""
    tokens = re.split(r'\W+', text)

    expected = set(['planeet', 'planetologie', 'kennis (wetenschap)',
                    'geomorfologie', 'Mars (planeet)'])
    concepts = set(string for _, _, string, _ in sem.all_candidates(tokens))

    assert_less_equal(expected, concepts)
