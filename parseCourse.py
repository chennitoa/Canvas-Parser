from canvasapi import Canvas
from requiredParameters import *
import json
import pprint as pp

API_URL = "https://sjsu.instructure.com"
API_KEY = "12~IzKPFz5iutKF9tbZk0WiaibY7uORLuEh2cha65VJzHoWFYrKyZh1bGcYuUUlQW6t"

canvas = Canvas(API_URL, API_KEY)
id = 1270511



course = canvas.get_course(id)

print('Course name is', course.name, "\nCourse id is", id)

# Update parameters given set, otherwise set to None
def update_parameters(dict_to_update, REQUIRED_PARAMETERS):
    """
    :type dict_to_update: dict
    :type REQUIRED_PARAMETERS: set
    :rtype: dict
    """
    updated_dict = {}
    for parameter in REQUIRED_PARAMETERS:
        if parameter in dict_to_update:
            updated_dict.update({parameter: dict_to_update[parameter]})
        else:
            updated_dict.update({parameter: None})
    return updated_dict

# Parse modules
modules = course.get_modules(include = ['items'])
updated_modules = []
for module in modules:
    module_dict = vars(module)
    # Create module object from given parameters
    module_object = update_parameters(module_dict, MODULE_REQUIRED_PARAMETERS)

    # Process each module item seperately
    module_items = module.get_module_items(include = ['content_details'])
    updated_module_items = []
    for module_item_object in module_items:
        module_item = vars(module_item_object)
        updated_module_item = update_parameters(module_item, MODULE_ITEM_REQUIRED_PARAMETERS)

        # Remove module item from list and append updated version
        updated_module_items.append(updated_module_item)
    
    module_object.update({'items': updated_module_items})
    updated_modules.append(module_object)

# Parse Assignment Groups
assignment_groups = course.get_assignment_groups()
updated_assignment_groups = []
for assignment_group in assignment_groups:
    assignment_group_dict = vars(assignment_group)
    updated_assignment_group = update_parameters(assignment_group_dict, ASSIGNMENT_GROUP_REQUIRED_PARAMETERS)
    updated_assignment_groups.append(updated_assignment_group)

# Parse Assignments
assigments = course.get_assignments()
updated_assignments = []
for assignment in assigments:
    assignment_dict = vars(assignment)
    updated_assignment = update_parameters(assignment_dict, ASSIGNMENT_REQUIRED_PARAMETERS)
    updated_assignments.append(updated_assignment)

# Parse Discussion Topics
discussion_topics = course.get_discussion_topics()
updated_discussion_topics = []
for discussion_topic in discussion_topics:
    discussion_topic_dict = vars(discussion_topic)
    updated_discussion_topic = update_parameters(discussion_topic_dict, DISCUSSION_TOPIC_REQUIRED_PARAMETERS)
    updated_discussion_topics.append(updated_discussion_topic)



course_dict = {
    'modules': updated_modules,
    'assignment_groups': updated_assignment_groups,
    'assignments': updated_assignments,
    'discussion_topics': updated_discussion_topics
    }


course_json = json.dumps(course_dict, indent = 4, default = str)
with open('course.json', 'w') as outfile:
    outfile.write(course_json)
    print("wrote to course_json")

