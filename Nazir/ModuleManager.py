import os
from importlib import *
MODULE_DIRECTORY = r"Nazir\modules"

def Load_Modules():
    list = []
    current_directory = os.getcwd()
    module_directory = os.path.join(current_directory,MODULE_DIRECTORY)
    for root, dirs, files in os.walk(module_directory):
        for file in files:
            filename = os.path.splitext(file)[0]
            if filename != '__init__' and filename != 'BaseModule':
                module = import_module('.'+filename,'Nazir.modules')
                print("Loading " + filename)