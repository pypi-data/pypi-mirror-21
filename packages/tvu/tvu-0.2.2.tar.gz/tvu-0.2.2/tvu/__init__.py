import pkg_resources
import sys


class TVUModule(object):

    def __init__(self, name):
        self.__name__ = name

        import tvu._tvu
        import tvu.tvus

        self.tvus = tvu.tvus

        self.TVU = tvu._tvu.TVU
        self.EnumTVU = tvu._tvu.EnumTVU

        self.instance = tvu._tvu.instance
        self.nullable = tvu._tvu.nullable

        self._validate_and_unify = tvu._tvu.validate_and_unify

        try:
            self.__version__ = pkg_resources.require('tvu')[0].version
        except pkg_resources.DistributionNotFound:
            self.__version__ = 'dev'

        self.__file__ = __file__

    def __call__(self, **kwargs):
        return self._validate_and_unify(**kwargs)


sys.modules[__name__] = TVUModule(__name__)
