import math

import numpy as np


class SDNML(object):
    def __init__(self, discounting_param=0.1, order=2):
        self.discounting_param = discounting_param
        self.order = order
        self._stats = dict(e_queue=[], tau=None)
        self._time = 1

    def _update_stats(self, x):
        n_features, _ = x.shape
        if 'v' not in self._stats:
            self._stats['v'] = np.random.rand(n_features, n_features)
        if 'm' not in self._stats:
            self._stats['m'] = np.random.rand(n_features, n_features)
        r = self.discounting_param  # alias
        c = r*x.T.dot(self._stats['v']).dot(x)
        a = self._stats['v'].dot(self._stats['m'])
        v = (1/(1-r))*self._stats['v'] \
            - (r/(1-r)) * \
            ((self._stats['v'].dot(x).dot(x.T).dot(self._stats['v']))/(1-r+c))
        m = (1-r)*self._stats['m']+r*x*x.T
        e = x-a.T.dot(x)
        d = c/(1-r+c)
        self._stats['c'] = c
        self._stats['a'] = a
        self._stats['v'] = v
        self._stats['m'] = m
        self._stats['d'] = d
        self._stats['e_queue'].append(e.T.dot(e))
        if self._time > self.order:
            tau = sum(self._stats['e_queue'])/(self._time-self.order)
            self._stats['prev_tau'] = self._stats['tau']
            self._stats['tau'] = tau

    def length(self, X):
        """Calculate SDNML code-length.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix of individual samples.

        Returns
        -------
        lengths : iterator, shape (n_samples, )
            Iterator of code lengths of the individuale samples.
        """
        for x in X:
            x = np.atleast_2d(x).T
            self._update_stats(x)
            if self._time <= self.order+1:
                yield 0
            else:
                code_length = (math.log(math.pi)/2) \
                              - math.log(1-self._stats['d'])
                code_length += math.log(
                    math.gamma((self._time-self.order-1)/2)
                )
                code_length -= math.log(math.gamma((self._time-self.order)/2))
                code_length += (math.log(self._time-self.order-1) +
                                math.log(self._stats['prev_tau']))/2
                code_length += (self._time-self.order)/2 * (
                    math.log((self._time-self.order)*self._stats['tau']) -
                    math.log((self._time-self.order-1)*self._stats['prev_tau'])
                )
                yield code_length
            self._time += 1
