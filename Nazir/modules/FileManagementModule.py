from Nazir.modules.BaseModule import BaseModule
from FileUtility import  *
FILEMANAGEMENT_MODULE_VERSION = '1.0.0'


class FileManagementModule(BaseModule):

    def __init__(self):
        self.module_version = FILEMANAGEMENT_MODULE_VERSION
        self.home_folder = ''
        self.download_folder =''

    def response(self, input_string):
        print("Response to User Input")

    def set_home_folder(self, home_folder):
        if is_dir(home_folder):
            self.home_folder = home_folder
        else:
            print("Folder Invalid")

    def set_download_folder(self, download_folder):
        self.download_folder = download_folder

    def sort_download(self):
        '''
        This function will sort the content of the download folder into home folder
        :param download_folder:
        :return:
        '''
        if self.home_folder is '':
            print("Home folder is not set")
            return 1
        if self.download_folder is '':
            print("Download folder is not set")
            return 1


