import os
from importlib import *
import Nazir.modules
MODULE_DIRECTORY = r"Nazir\modules"


def Load_Modules():
    """
    Load Nazir Module, return a list of module object
    :return:
    """
    module_list = []
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
                module_list.append(module_object)
    return module_list


def module_check(module_list):
    has_communication_module = False
    has_kernel_module = False
    for module in module_list:
        if module.__class__.__name__ == "CommunicationModule":
            has_communication_module = True
        if module.__class__.__name__ == "KernelModule":
            has_kernel_module = True
    return has_communication_module and has_kernel_module
