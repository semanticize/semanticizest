"""parse_wikidump

Usage:
    parse_wikidump [options] <dump> <model-filename>

Options:
    --download=wikiname     Download dump from dumps.wikimedia.org first
    --ngram=order, -N order Maximum order of ngrams
                            [default 7, None to disable]
    --help, -h              This help
"""
from __future__ import print_function

import logging
import sqlite3
import sys

from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlretrieve

from docopt import docopt

from . import parse_dump
from .._semanticizer import createtables_path


logger = logging.getLogger('semanticizest')
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel('INFO')


class Progress(object):
    def __init__(self):
        self.threshold = .0

    def __call__(self, n_blocks, blocksize, totalsize):
        done = n_blocks * blocksize
        if done >= self.threshold * totalsize:
            logger.info("%3d%% done", int(100 * self.threshold))
            self.threshold += .05


DUMP_TEMPLATE = (
    "https://dumps.wikimedia.org/{0}/latest/{0}-latest-pages-articles.xml.bz2")


def main(args):
    args = docopt(__doc__, args)

    wikidump = args['<dump>']
    if args["--download"]:
        url = DUMP_TEMPLATE.format(args["--download"])
        logger.info("Saving wikidump to %r", wikidump)
        try:
            urlretrieve(url, wikidump, Progress())
        except HTTPError as e:
            print("Cannot download {0!r}: {1}".format(url, e))
            sys.exit(1)

    model_fname = args['<model-filename>']
    ngram = args['--ngram']
    if ngram not in (None, "None"):
        ngram = int(ngram)

    db = sqlite3.connect(model_fname)
    with open(createtables_path()) as f:
        create = f.read()

    c = db.cursor()
    c.executescript(create)

    parse_dump(wikidump, db, N=ngram)
    db.close()


if __name__ == '__main__':
    main(sys.argv[1:])
