import abc

class BaseModule(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.module_version = ''
    @abc.abstractproperty
    def command_list(self):
        return 'Error'

    def get_version(self):
        """
        Get module's version
        :return:
        """
        return self.module_version

    def get_command_list(self):
        return self.command_list


