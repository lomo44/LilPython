import os
from importlib import *
import Nazir.modules
MODULE_DIRECTORY = r"Nazir\modules"

# Global module list, contains all the module loaded in to Nazir
GLOBAL_MODULE_LIST = []
ESSENTIAL_MODULE_LIST = [
]

def Load_Modules():
    """
    Load Nazir Module, return a list of module object
    :return:
    """
    current_directory = os.getcwd()
    module_directory = os.path.join(current_directory,MODULE_DIRECTORY)
    for root, dirs, files in os.walk(module_directory):
        for file in files:
            filename = os.path.splitext(file)[0]
            if filename != '__init__' and filename != 'BaseModule':
                module = import_module('.'+filename,'Nazir.modules')
                print("Loading " + filename)
                module_class = getattr(module,filename)
                module_object = module_class()
                GLOBAL_MODULE_LIST.append(module_object)


def module_check():
    module_list = ESSENTIAL_MODULE_LIST.copy()
    for module in GLOBAL_MODULE_LIST:
        if module.__class__.__name__ in module_list:
            module_list.remove(module.__class__.__name__)
    return len(module) is 0


