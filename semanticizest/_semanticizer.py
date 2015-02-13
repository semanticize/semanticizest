from collections import defaultdict
import sqlite3
from os.path import join, dirname, abspath

import six

from semanticizest._util import ngrams_with_pos, tosequence
from semanticizest.parse_wikidump import parse_dump


class Semanticizer(object):
    """Entity linker.

    Parameters
    ----------
    fname : string
        Filename of the stored model from which to load the
        Wikipedia statistics.

    """

    def __init__(self, fname):
        """Create a semanticizer from a stored model."""
        commonness = defaultdict(list)

        self.db = sqlite3.connect(fname)
        self._cur = self.db.cursor()

        for target, anchor, count in self._get_senses_counts():
            commonness[anchor].append((target, count))

        for anchor, targets in six.iteritems(commonness):
            # targets.sort(key=operator.itemgetter(1), reverse=True)

            # Turn counts into probabilities.
            # XXX should we preserve the counts as well?
            total = float(sum(count for _, count in targets))
            commonness[anchor] = [(t, count / total) for t, count in targets]

        self.commonness = commonness
        self.N = self._get_ngram_max_length()

    def _get_ngram_max_length(self):
        self._cur.execute("select value "
                          "from parameters "
                          "where key = 'N';")
        N = self._cur.fetchone()[0]
        if N == 'None':
            N = None
        else:
            N = int(N)
        return N

    def _get_senses_counts(self):
        """Return all senses and their counts."""
        return self._cur.execute('select target, ngram as anchor, count '
                                 'from linkstats, ngrams '
                                 'where ngram_id = ngrams.id;')

    def all_candidates(self, s):
        """Retrieve all candidate entities.

        Parameters
        ----------
        s : {string, iterable over string}
            Tokens. If a string, it will be tokenized using a naive heuristic.

        Returns
        -------
        candidates : iterable over (int, int, string, float)
            Candidate entities are 4-tuples of the indices `start` and
            `end` (both in tokenized input, and both start at 1),
            `target entity` (title of the Wikipedia article) and
            `probability` (commonness.)
        """

        if isinstance(s, six.string_types):
            # XXX need a smarter tokenizer!
            s = s.split()
        else:
            s = tosequence(s)

        for i, j, s in ngrams_with_pos(s, self.N):
            if s in self.commonness:
                for target, prob in self.commonness[s]:
                    yield i, j, target, prob


def create_model(dump, db_file=':memory:', N=2):
    """Create a semanticizer model from a wikidump and store it in a DB.

    Parameters
    ----------
    dump : string
        Filename of a Wikipedia dump, e.g.,
        'enwiki-20141106-pages-articles.xml.bz2'
    db_file : string
       (File)name of the sqlite3 DB. If `df_file` is `:memory:`, an in-memory
       db will be created, otherwise it is the filename of the
       disk-based db.

    Returns
    ------
    db : sqlite3.Connection
        The handle to the newly created db containing the model.
    """
    db = sqlite3.connect(db_file)
    _parse_stuff_to_db(dump, db, N=N)
    return db


def _parse_stuff_to_db(fname, db, N=2):
    """Parses a wikidump, stores the model supplied db."""
    cur = db.cursor()
    with open(createtables_path()) as create:
        cur.executescript(create.read())
    dump = join(dirname(abspath(__file__)),
                fname)
    parse_dump(dump, db, N=N)

    return db


def createtables_path():
    """Return the full path to the DB initialization script."""
    return join(dirname(__file__), "createtables.sql")
