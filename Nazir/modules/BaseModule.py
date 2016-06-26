import abc


class BaseModule(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractproperty
    def module_version(self):
        return 'Error'

    def get_version(self):
        """
        Get module's version
        :return:
        """
        return self.module_version

    @abc.abstractclassmethod
    def response(self):
        """User Input Response"""

