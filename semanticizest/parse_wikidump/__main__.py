"""parse_wikidump

Usage:
    parse_wikidump [options] <dump> <model-filename>
    parse_wikidump [options] --download=<wikiname> <dump> <model-filename>

Options:
    --ngram=order, -N order Maximum order of ngrams
                      [default 7, None to disable]
    --help, -h              This help
"""
from __future__ import print_function

from os.path import dirname, join
import sqlite3

from six.moves.urllib.request import urlopen

from docopt import docopt
from .._wiki_dump_parser import parse_dump


def main(args):
    wikidump = args['<dump>']
    if args["--download"]:
        url = "https://dumps.wikimedia.org/{0}/latest/{0}-latest-pages-articles.xml.bz2".format(args["--download"])
        dumpstream = urlopen(url) # Can give a HTTPError in case of 404
        # Probably want to print or log something here
        with open(wikidump, "w") as out:
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

    parse_dump(wikidump, db, N=ngram, verbose=True)
    db.close()


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
