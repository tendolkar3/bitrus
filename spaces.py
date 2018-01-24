

class BoxSpace(object):
    """
    a generic space object for both the action space and the observation space
    """
    def __init__(self, low, high, shape=None):
        """
        the action space is a numpy array of the given shape
        :param low: takes an np.array
        :param high: takes an np.array
        :param shape: tuple
        """
        if shape is None:
            assert low.shape == high.shape
            self.low = low
            self.high = high
        else:
            assert np.isscalar(low) and np.isscalar(high)
            self.low = low + np.zeros(shape)
            self.high = high + np.zeros(shape)

    def contains(self, x):
        return x.shape == self.shape and (x >= self.low) and (x <= self.high)

    def sample(self):
        return np.random.uniform(low=self.low, high=self.high, size=self.shape)

    @property
    def shape(self):
        return self.low.shape


class DiscreteSpace(object):

    def __init__(self, n):

        self.n = n

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.kind in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int >= 0 and as_int < self.n

    def sample(self):
        return np.random.randint(self.n)

    @property
    def shape(self):
        return self.n


class Tuple(object):

    def __init__(self):
        pass

