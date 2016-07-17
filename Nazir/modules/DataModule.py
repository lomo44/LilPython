import pickle
from FileUtility import *

from Nazir.modules.BaseModule import BaseModule
from Nazir.modules.config import *
DATA_MODULE_MODULE_VERSION = '1.0.0'
DATA_SET_FILE_EXTENSION = '.catset'
CATEGORY_LIST_NAME = 'catlist'
CATEGORY_DEPOT_LOCATION = 'data_depot'

def DataModulePrint(string):
    print("Data Module: "+string)

class CategorySet:
    def __init__(self, name):
        self.m_name = name
        self.m_items = []
        self.m_storinglocation = ""
    def add(self, name):
        if name not in self.m_items:
            self.m_items.append(name)
    def get_set(self):
        return self.m_items
    def remove(self, name):
        if name in self.m_items:
            self.m_items.remove(name)
    def has_item(self, name):
        return name in self.m_items
    def save_category_file(self, location):
        self.m_storinglocation = location
        self.update_category_file()
    @staticmethod
    def load_category_file(category_file_location):
        if checkFileExist(category_file_location) and is_file(category_file_location):
            with open(category_file_location, 'rb') as file:
                cfile = pickle.load(file)
                return cfile
        else:
            return None
    def get_category_full_path(self):
        return os.path.join(self.m_storinglocation, self.m_name + DATA_SET_FILE_EXTENSION)
    def update_category_file(self):
        file_name = os.path.join(self.m_storinglocation, self.m_name + DATA_SET_FILE_EXTENSION)
        with open(file_name,'wb+') as file:
            pickle.dump(self,file,pickle.HIGHEST_PROTOCOL)

class DataModule(BaseModule):

    def __init__(self):
        self.module_version = DATA_MODULE_MODULE_VERSION
        self.m_people = {}
        self.m_categorynamelist = None
        self.m_categoryobjectlist = []
        self.m_datadepotlocation = ""

    def initialize(self):
        def first_time_initialize():
            DataModulePrint('Local data config not found, creating one')
            self.m_categorynamelist = CategorySet(CATEGORY_LIST_NAME)
            self.m_categorynamelist.save_category_file(self.m_datadepotlocation)

        self.m_datadepotlocation = os.path.join(HOME_DIRECTORY, CATEGORY_DEPOT_LOCATION)
        category_list_full_name = CATEGORY_LIST_NAME + DATA_SET_FILE_EXTENSION
        category_list_path = os.path.join(self.m_datadepotlocation, category_list_full_name)
        if checkDirectoryExist(self.m_datadepotlocation):
            if file_valid(category_list_path):
                DataModulePrint('Local Data config file found, loading...')
                self.load_categorylist(category_list_path)
            else:
                first_time_initialize()
        else:
            # First Time Initialization
            os.mkdir(self.m_datadepotlocation)
            first_time_initialize()
        # Loading category in the category list
        # self.load_categories(self.m_datadepotlocation)
        DataModulePrint('Initialization Complete')

    def uninitialize(self):
        self.m_categorynamelist.update_category_file()
        for category in self.m_categoryobjectlist:
            category.update_category_file()

    def response(self, input_string):
        DataModulePrint("User Response")

    def load_categorylist(self, category_list_path):
        self.m_categorynamelist = CategorySet.load_category_file(category_list_path)

    def load_categories(self, data_depot_location):
        for category_name in self.m_categorynamelist.get_set():
            category_full_name = category_name + DATA_SET_FILE_EXTENSION
            category_location = os.path.join(data_depot_location, category_full_name)
            if file_valid(category_location):
                self.m_categoryobjectlist.append(CategorySet.load_category_file(category_location))
            else:
                DataModulePrint("Category: " + category_name + " not found")

    def save_category(self, category_depot_location):
        for category in self.m_categoryobjectlist:
            category.update_category_file()

    def add_catagory(self, name):
        DataModulePrint("adding catagory")
        newcategory = CategorySet(name)
        newcategory.save_category_file(self.m_datadepotlocation)
        self.m_categoryobjectlist.append(newcategory)
        self.m_categorynamelist.add(name)
        self.m_categorynamelist.update_category_file()

    def delete_category(self, name):
        for category in self.m_categoryobjectlist:
            if category.m_name == name:
                self.m_categoryobjectlist.remove(category)
                removefile(category.get_category_full_path())

        for category_name in self.m_categorynamelist.get_set():
            if category_name == name:
                self.m_categorynamelist.remove(category_name)
        self.m_categorynamelist.update_category_file()
        DataModulePrint('Deleting category')

    def search_category(self, name):
        for category in self.m_categoryobjectlist:
            if category.m_name == name:
                return category
        DataModulePrint('Searching category ')


if __name__ == '__main__':
    test = DataModule()
    test.initialize()
    test.add_catagory('test')
    test.delete_category('test')
    test.uninitialize()