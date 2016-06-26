from Nazir.modules.BaseModule import BaseModule
KERNEL_MODULE_VERSION = '1.0.0'


class KernelModule(BaseModule):
    """
    Basic kernel module, use for control all the module operation
    """
    def __init__(self):
        self.module_version = KERNEL_MODULE_VERSION

    def response(self):
        print("Response to User Input")
