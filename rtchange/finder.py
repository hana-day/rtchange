from .coding import SDNML


class Finder(object):
    def __init__(self, discounting_param=0.1, order=2, smoothing=10,
                 code_length_class='sdnml'):
        self.discounting_param = discounting_param
        self.order = order
        self.smoothing = smoothing
        if code_length_class == 'sdnml':
            self.first_code_length = SDNML(
                discounting_param=discounting_param,
                order=order)
            self.second_code_length = SDNML(
                discounting_param=discounting_param,
                order=order)
        else:
            raise ValueError("Unknown code-length class {:s}".format(
                code_length_class))
        self._first_score_queue = [0 for _ in range(smoothing)]
        self._second_score_queue = [0 for _ in range(smoothing)]

    def score_one(self, x):
        """Calculate a change score.

        Parameters
        ----------
        x : float
            The sample you want to calculate the change score.

        Returns
        -------
        score : float
            Change score of the sample.
        """
        self._first_score_queue.pop(0)
        self._first_score_queue.append(self.first_code_length.length(x))
        first_smoothed = sum(self._first_score_queue)/self.smoothing
        self._second_score_queue.pop(0)
        self._second_score_queue.append(
            self.second_code_length.length(first_smoothed))
        score = sum(self._second_score_queue)/self.smoothing
        return score

    def score(self, X):
        """Calculate change scores.

        Parameters
        ----------
        X : array-like, shape (1, n_samples)
            Sequence of the samples.

        Returns
        -------
        scores : iterator shale(n_samples)
            Change scores of the individuale samples.
        """
        for x in X:
            yield self.score_one(x)
