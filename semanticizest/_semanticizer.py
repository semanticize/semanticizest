from collections import defaultdict
import sqlite3
from os.path import join, dirname, abspath

import six

from math import sqrt
from scipy.stats import norm 

from semanticizest._util import ngrams_with_pos, tosequence
from semanticizest.parse_wikidump import parse_dump


class Semanticizer(object):
    """Entity linker.

    Parameters
    ----------
    fname : string
        Filename of the stored model from which to load the
        Wikipedia statistics.

    N : int
        Maximum length of the ngrams to extract from the token
        sequences. This should be the same as the length used to
        create the stored model.
    """

    def __init__(self, fname, N=7, score='wilson', wilson_confidence=0.95):
        commonness = defaultdict(list)

        self.db = sqlite3.connect(fname)
        cur = self.db.cursor()
        for target, anchor, count in cur.execute(
            'select target, ngram as anchor, count '
            'from linkstats, ngrams '
            'where ngram_id = ngrams.id;'):
            commonness[anchor].append((target, count))

        if score=='wilson':
            # Better but slower
            z = norm.ppf(wilson_confidence)
            makeProb = lambda count, total: self._ci_lower_bound(count, total, z)
        else:
            makeProb = lambda count, total: count / total

        for anchor, targets in six.iteritems(commonness):
            # targets.sort(key=operator.itemgetter(1), reverse=True)

            # Turn counts into probabilities.
            # XXX should we preserve the counts as well?
            total = float(sum(count for _, count in targets))
            commonness[anchor] = [(t, makeProb(count, total)) for t, count in targets]

        self.commonness = commonness
        self.N = N

    def _ci_lower_bound(self, pos, n, z):
        """
        Calculate Lower bound of Wilson score confidence interval for a Bernoulli parameter
        as described here: 
        http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
        """
        if n == 0:
            return 0
        phat = 1.0*pos/n
        score = (phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
        return score

    def all_candidates(self, s):
        """Retrieve all candidate entities.

        Parameters
        ----------
        s : {string, iterable over string}
            Tokens. If a string, it will be tokenized using a naive heuristic.

        Returns
        -------
        candidates : iterable over (int, int, string, float)
            Candidate entities: 4-tuples of start index, end index
            (both in tokenized input), target entity and probability
            (commonness).
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


def create_model(dump, db_file=':memory:'):
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
    _parse_stuff_to_db(dump, db)
    return db


def _parse_stuff_to_db(fname, db):
    """Parses a wikidump, stores the model supplied db."""
    cur = db.cursor()
    with open(createtables_path()) as create:
        cur.executescript(create.read())
    dump = join(dirname(abspath(__file__)),
                fname)
    parse_dump(dump, db, N=2)

    return db


def createtables_path():
    """Return the full path to the DB initialization script."""
    return join(dirname(__file__), "createtables.sql")
