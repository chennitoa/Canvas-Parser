from canvasapi import Canvas
from requiredParameters import *
import json
import pprint as pp

API_URL = "https://sjsu.instructure.com"
API_KEY = "12~IzKPFz5iutKF9tbZk0WiaibY7uORLuEh2cha65VJzHoWFYrKyZh1bGcYuUUlQW6t"
canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(1270511)
print('Now, course name is ', course.name)

file = open("modules.json", "r")

created_modules = []

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

file.close()