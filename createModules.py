from canvasapi import Canvas
from requiredParameters import *
import json
import pprint as pp

file = 'modules.json'

created_modules = []

with open(file, 'r') as infile:
    course_attributes = json.load(file)
    modules = course_attributes['modules']

for module in modules:
    module_args = {}
    for parameter in MODULE_REQUIRED_PARAMETERS:
        if parameter in module:
            module_args.update({parameter: module[parameter]})
    
    new_module = course.create_module(module_args)
    created_modules.append(new_module)
    
    print('module[items] is', module['items'])
    for item in module['items']:
        new_module_item = {}
        for parameter in MODULE_ITEM_REQUIRED_PARAMETERS:
            if parameter in item:
                new_module_item.update({parameter: item[parameter]})

        # With all parameters, create the module item
        new_module.create_module_item(new_module_item)
        print('Created new module item:', new_module_item)