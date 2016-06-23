import abc


class BaseModule(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def load(self):
        """Load Module"""
    @abc.abstractclassmethod
    def response(self):
        """User Input Response"""

