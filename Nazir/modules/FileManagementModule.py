from Nazir.modules.BaseModule import BaseModule
FILEMANAGEMENT_MODULE_VERSION = '1.0.0'


class FileManagementModule(BaseModule):

    def __init__(self):
        self.module_version = FILEMANAGEMENT_MODULE_VERSION

    def response(self):
        print("Response to User Input")
