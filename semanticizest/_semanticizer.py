from collections import defaultdict
import operator

import six

from semanticizest._util import ngrams_with_pos, tosequence


class Semanticizer(object):
    def __init__(self, link_count, N=7):
        commonness = defaultdict(list)

        for (target, anchor), count in six.iteritems(link_count):
            commonness[anchor].append((target, count))
        for anchor, targets in six.iteritems(commonness):
            # targets.sort(key=operator.itemgetter(1), reverse=True)

            # Turn counts into probabilities.
            # XXX should we preserve the counts as well?
            total = float(sum(count for _, count in targets))
            commonness[anchor] = [(t, count / total) for t, count in targets]

        self.commonness = commonness
        self.N = N

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
