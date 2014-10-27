from __future__ import print_function

from os.path import dirname, join
import sqlite3
import sys

from .._wiki_dump_parser import parse_dump


if len(sys.argv) != 3:
    print('usage: %s dump model.db' % sys.argv[0], file=sys.stderr)
    sys.exit(1)


db = sqlite3.connect(sys.argv[2])
with open(join(dirname(__file__), "createtables.sql")) as f:
    create = f.read()
c = db.cursor()
c.executescript(create)

c.execute('pragma synchronous = off')

parse_dump(sys.argv[1], db, verbose=True)
