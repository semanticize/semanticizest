# -*- coding: utf-8 -*-

from cytoolz import compose

from os.path import abspath, dirname, join
import sqlite3
import tempfile

from nose.tools import (assert_equal, assert_greater, assert_in, assert_not_in)

import semanticizest.parse_wikidump
from semanticizest.parse_wikidump.__main__ import main as parse_wikidump_main
from semanticizest._wiki_dump_parser import (clean_text, extract_links,
                                             page_statistics, parse_dump,
                                             remove_links)


# Straight from nlwiki: a {| {| |} table (works in MediaWiki!)
unclosed_table = '''
Nikkel wordt verhandeld op beurzen zoals de London Metal Exchange.
Dagelijks komen vraag en aanbod bij elkaar en komt een prijs tot stand.
In de onderstaande tabel de gemiddelde prijs van nikkel per jaar.
{| {| class=&quot;wikitable&quot; style=&quot;text-align: center&quot;
!Omschrijving
!2005
!2006
!2007
!2008
!2009
!2010
!2011
|-
|Nikkelprijs ($/ton)|| 14.733|| 24.267|| 37.181 || 21.027 || 14.700 ||21.809 || 22.831
|}
This is not in the original.'''


def test_clean_text():
    out = clean_text(unclosed_table).splitlines()
    expected = (unclosed_table.splitlines()[:4]
                + ['']
                + unclosed_table.splitlines()[-1:])
    assert_equal(out, expected)


def test_extract_links():
    first_link = compose(tuple, next, iter, extract_links)

    assert_equal(first_link("[[foo|bar]]"), ("foo", "bar"))
    assert_equal(first_link("[[foo]]"), ("foo", "foo"))
    assert_equal(first_link("[[File:picture!]] [[foo]]"), ("foo", "foo"))
    assert_equal(first_link("[[foo]]bar."), ("foo", "foobar"))
    assert_equal(first_link("[[baz|foobar]];"), ("baz", "foobar"))
    assert_equal(first_link("[[baz#quux]]"), ("baz", "baz#quux"))
    assert_equal(first_link("[[baz#quux|bla]]"), ("baz", "bla"))

    # This construct appears in enwiki for chemical formulae etc., but also in
    # nlwiki (and dewiki?) for more general compound nouns. The current
    # handling may not be exactly what we want; any fix should update the test
    # accordingly.
    assert_equal(list(extract_links("[[Lithium|Li]][[Fluorine|F]]")),
                 [("Lithium", "Li"), ("Fluorine", "F")])
    assert_equal(list(extract_links("[[tera-|tera]][[becquerel]]s")),
                 [("tera-", "tera"), ("becquerel", "becquerels")])


def test_page_statistics():
    page = """
        Wikisyntax is the [[syntax (to be parsed)|syntax]] used on
        [[Wikipedia]].{{citation needed|date=October 2014}}
        We have to parse it, and we use every [[hack]] in the
        [[text]][[book]] that we can find.

        And now, for something [[Wikipedia|completely]] [[hack|different]].

        Let's repeat the [[text]] to get more interesting [[statistic]]s.
        And the [[book]] too.
    """

    expected_links = {('syntax (to be parsed)', 'syntax'): 1,
                      ('Wikipedia', 'Wikipedia'): 1,
                      ('hack', 'hack'): 1,
                      ('text', 'text'): 2,
                      ('book', 'book'): 2,
                      ('Wikipedia', 'completely'): 1,
                      ('hack', 'different'): 1,
                      ('statistic', 'statistics'): 1}

    links, ngrams = page_statistics(page, N=2)

    assert_equal(dict(links), expected_links)

    assert_in('And now', ngrams)
    assert_not_in('Wikipedia We', ngrams)
    assert_not_in('find. And', ngrams)
    assert_not_in('find And', ngrams)


def test_parse_dump_ngrams():
    db = sqlite3.connect(':memory:')
    cur = db.cursor()
    with open(join(dirname(semanticizest.parse_wikidump.__file__),
                   "createtables.sql")) as create:
        cur.executescript(create.read())

    dump = join(dirname(abspath(__file__)),
                'nlwiki-20140927-pages-articles-sample.xml')
    parse_dump(dump, db, N=2)

    ngram_count = dict(cur.execute('select ngram, tf from ngrams;'))
    link_count = dict(cur.execute('select target, count from linkstats;'))

    assert_in(ur'van München', ngram_count)
    assert_in(u'Vrede van M\xfcnster', link_count)
    #assert_greater(link_count[('AMX Index', 'Amsterdam Midkap Index')], 0)
    assert_greater(link_count['AMX Index'], 0)


def test_parse_dump():
    db = sqlite3.connect(':memory:')
    cur = db.cursor()
    with open(join(dirname(semanticizest.parse_wikidump.__file__),
                   "createtables.sql")) as create:
        cur.executescript(create.read())

    dump = join(dirname(abspath(__file__)),
                'nlwiki-20140927-pages-articles-sample.xml')
    parse_dump(dump, db, N=None)

    ngram_count = dict(cur.execute('select ngram, tf from ngrams;'))
    link_count = dict(cur.execute('select target, count from linkstats;'))

    assert_in('Heinrich Tessenow', ngram_count)
    assert_in('Heinrich Tessenow', link_count)


def test_parse_wikidump():
    tmpfile = 'abcdefXXXXX'
    dump = join(dirname(abspath(__file__)),
                'nlwiki-20140927-pages-articles-sample.xml')
    with tempfile.NamedTemporaryFile(tmpfile) as model_file:
        args = {'--ngram': 2,
                '<model-filename>': model_file.name,
                '<dump>': dump}
        parse_wikidump_main(args)

        db = sqlite3.connect(model_file.name)
        cur = db.cursor()
        actual = list(cur.execute('select count(*) from ngrams;'))[0][0]
        expected = 22860
        assert_equal(actual, expected)


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
