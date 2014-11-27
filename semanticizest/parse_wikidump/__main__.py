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
from os.path import dirname, join
import sqlite3
import sys

from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlopen

from docopt import docopt

from . import parse_dump


logger = logging.getLogger('semanticizest')
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel('INFO')

DUMP_TEMPLATE = (
    "https://dumps.wikimedia.org/{0}/latest/{0}-latest-pages-articles.xml.bz2")


def main(args):
    args = docopt(__doc__, args)

    wikidump = args['<dump>']
    if args["--download"]:
        url = DUMP_TEMPLATE.format(args["--download"])
        try:
            dumpstream = urlopen(url)
        except HTTPError as e:
            print("Cannot download {0!r}: {1}".format(url, e))
            sys.exit(1)
        # Probably want to print or log something here
        with open(wikidump, "w") as out:
            logger.info("Saving wikidump to %r", wikidump)
            out.write(dumpstream.read())

    model_fname = args['<model-filename>']
    ngram = args['--ngram']
    if ngram not in (None, "None"):
        ngram = int(ngram)

    db = sqlite3.connect(model_fname)
    with open(join(dirname(__file__), "createtables.sql")) as f:
        create = f.read()

    c = db.cursor()
    c.executescript(create)

    parse_dump(wikidump, db, N=ngram)
    db.close()


if __name__ == '__main__':
    main(sys.argv)
