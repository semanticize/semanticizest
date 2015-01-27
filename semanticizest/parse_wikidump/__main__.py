"""parse_wikidump

Usage:
    parse_wikidump [options] <dump> <model-filename>
    parse_wikidump --download=<wikiname> <model-filename>

Options:
    --download=wikiname     Download dump from dumps.wikimedia.org first
    --ngram=<order>, -N <order>
                            Maximum order of ngrams, set to None to disable
                            [default: 7]
    --help, -h              This help
"""
from __future__ import print_function

import logging
import re
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


def die(msg):
    print("semanticizest.parse_wikidump: %s" % msg, file=sys.stderr)
    sys.exit(1)


def main(args):
    args = docopt(__doc__, args)

    if args["--download"]:
        wikidump = args["--download"] + ".xml.bz2"
    else:
        wikidump = args['<dump>']

    model_fname = args['<model-filename>']
    ngram = args['--ngram']
    if ngram == "None":
        ngram = None
    else:
        ngram = int(ngram)

    logger.info("Creating database at %r" % model_fname)
    try:
        db = sqlite3.connect(model_fname)
    except sqlite3.OperationalError as e:
        if 'unable to open' in str(e):
            # This exception doesn't store the path.
            die("%s: %r" % (e, model_fname))
    with open(createtables_path()) as f:
        create = f.read()

    c = db.cursor()
    try:
        c.executescript(create)
    except sqlite3.OperationalError as e:
        if re.search(r'table .* already exists', str(e)):
            die("database %r already populated" % model_fname)

    if args["--download"]:
        url = DUMP_TEMPLATE.format(args["--download"])
        logger.info("Saving wikidump to %r", wikidump)
        try:
            urlretrieve(url, wikidump, Progress())
        except HTTPError as e:
            die("Cannot download {0!r}: {1}".format(url, e))

    parse_dump(wikidump, db, N=ngram)
    db.close()


if __name__ == '__main__':
    main(sys.argv[1:])
