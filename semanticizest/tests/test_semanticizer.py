import os.path

from nose import SkipTest

from semanticizest import Semanticizer
from semanticizest._wiki_dump_parser import parse_dump


def test_semanticizer():
    raise SkipTest()
    here = os.path.dirname(os.path.abspath(__file__))
    dump = os.path.join(here, 'nlwiki-20140927-pages-articles-sample.xml')
    link_count, ngram_count = parse_dump(dump, N=2)

    sem = Semanticizer(link_count)
