from Nazir.modules.BaseModule import BaseModule
COMMUNICATION_MODULE_VERSION = "1.0.0"

class CommunicationModule(BaseModule):
    """
    Basic communication module, use for parsing and user interaction
    """
    def __init__(self):
        self.module_version = COMMUNICATION_MODULE_VERSION

    def response(self):
        print("Response to User Input")

