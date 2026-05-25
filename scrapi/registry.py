import sys


class _Registry(dict):

    # These must be defined so that doctest gathering doesn't make
    # pytest crash when trying to figure out what/where scrapi.registry is
    __file__ = __file__
    __name__ = __name__

    def __init__(self):
        dict.__init__(self)

    def __hash__(self):
        return hash(self.freeze(self))

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            raise KeyError('No harvester named "{}"'.format(key))



sys.modules[__name__] = _Registry()
