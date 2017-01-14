import pytest


class TestFinder(object):
    @pytest.fixture
    def finder(self):
        from rtchange.finder import Finder
        return Finder(discounting_param=0.1, order=3,
                      smoothing=3, code_length_class='sdnml')

    def test_score(self, finder):
        # After long 1, suddenly input 2.
        # So, the change score of the last 1 must be lower than
        # the score of the last 2.
        ones_length = 1000
        ones = [1 for _ in range(ones_length)]
        ones_last_score = list(finder.score(ones))[-1]
        twos_length = 10
        twos = [2 for _ in range(twos_length)]
        twos_last_score = list(finder.score(twos))[-1]
        assert ones_last_score < twos_last_score
