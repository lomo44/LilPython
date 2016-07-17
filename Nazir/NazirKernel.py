from Nazir.modules.BaseModule import BaseModule
KERNAL_MODULE_VERSION = "1.0.0"

GLOBAL_COMMAND_LIST = []

HOME_DIRECTORY = ""

class NazirKernel():
    """
    Basic communication module, use for parsing and user interaction
    """
    def __init__(self):
        self.module_version = KERNAL_MODULE_VERSION

    #def load_command(self, command_list):




