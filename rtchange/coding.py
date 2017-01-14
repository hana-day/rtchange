import abc
import math

import numpy as np


class CodeLength(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def length(self, x):
        pass


def zero2small(v, small=1e-5):
    return v if v > 0 else small


class SDNML(CodeLength):
    def __init__(self, discounting_param=0.1, order=2):
        self.discounting_param = discounting_param
        self.order = order
        self._stats = dict(e2_sum=0, tau=np.atleast_2d(0.1).T)
        self._xs = [0 for _ in range(self.order)]
        self._time = 1

    def _update_stats(self, xs):
        if 'v' not in self._stats:
            self._stats['v'] = np.full(
                (self.order, self.order), 1/self.order)
        if 'm' not in self._stats:
            self._stats['m'] = np.full(
                (self.order, self.order), 1/self.order)
        r = self.discounting_param  # alias
        c = r*xs.T.dot(self._stats['v']).dot(xs)
        v = (1/(1-r))*self._stats['v']
        v -= (
            (r/(1-r)) *
            (self._stats['v'].dot(xs).dot(xs.T).dot(self._stats['v']))/(1-r+c))
        m = (1-r)*self._stats['m']+r*xs*xs.T
        a = v.dot(m)
        e = xs-a.T.dot(xs)
        d = c/(1-r+c)
        self._stats['c'] = c
        self._stats['a'] = a
        self._stats['v'] = v
        self._stats['m'] = m
        self._stats['d'] = d
        self._stats['e2_sum'] += e.T.dot(e)
        tau = self._stats['e2_sum']/self._time
        self._stats['prev_tau'] = self._stats['tau']
        self._stats['tau'] = tau

    def length(self, x):
        """Calculate SDNML code-length.

        Parameters
        ----------
        x : float
            Sample.

        Returns
        -------
        code_length : float
            Code length of the sample.
        """
        self._xs.pop(0)
        self._xs.append(x)
        xs = np.atleast_2d(self._xs).T
        self._update_stats(xs)
        code_length = 0
        if self._time > 1:
            code_length = (math.log(math.pi)/2) \
                          - math.log(zero2small(1-self._stats['d']))
            code_length -= math.lgamma((self._time-1)/2)
            code_length += math.lgamma((self._time)/2)
            code_length += (math.log(self._time-1) +
                            math.log(zero2small(self._stats['prev_tau'])))/2
            code_length += (self._time)/2 * (
                math.log(zero2small((self._time)*self._stats['tau'])) -
                math.log(zero2small((self._time-1)*self._stats['prev_tau']))
            )
        self._time += 1
        return code_length
