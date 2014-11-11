"""parse_wikidump

Usage:
    parse_wikidump [options] <dump> <model-filename>

Options:
    --ngram=order, -N=order Maximum order of the ngrams to extract [default: 7]
    --help, -h              This help
"""
from __future__ import print_function

from os.path import dirname, join
import sqlite3

from docopt import docopt
from .._wiki_dump_parser import parse_dump


def main(args):
    wikidump = args['<dump>']
    model_fname = args['<model-filename>']
    ngram = int(args['--ngram'])

    db = sqlite3.connect(model_fname)
    with open(join(dirname(__file__), "createtables.sql")) as f:
        create = f.read()
    c = db.cursor()
    c.executescript(create)
    c.execute('pragma synchronous = off')

    parse_dump(wikidump, db, N=ngram, verbose=True)
    db.close()


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
