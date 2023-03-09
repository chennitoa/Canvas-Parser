from canvasapi import Canvas
from canvasParameters import *
import json


# Update parameters given set, otherwise set to None
def update_parameters(dict_to_update, REQUIRED_PARAMETERS, OPTIONAL_PARAMETERS):
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
    for parameter in OPTIONAL_PARAMETERS:
        if parameter in dict_to_update and not dict_to_update[parameter] is None:
            updated_dict.update({parameter: dict_to_update[parameter]})

    return updated_dict

class CourseParser:
    def __init__(self, course):
        """
        This class maintains a map of temporary ids.

        Attributes:
            course (canvasapi.course.Course): The course that is being parsed
            temporary_ids (dict): Map of content ids to temporary ids
        """
        
        self.course = course
        self.temporary_ids = {}

    # Parse modules
    def parse_modules(self):
        """
        :rtype: List[dict]
        """
        modules = self.course.get_modules(include = ['items'])
        updated_modules = []
        for module in modules:
            module_dict = vars(module)
            # Create module object from given parameters
            updated_module = update_parameters(module_dict, MODULE_REQUIRED_PARAMETERS, MODULE_OPTIONAL_PARAMETERS)

            # Process each module item seperately
            module_items = module.get_module_items(include = ['content_details'])
            updated_module_items = []
            for module_item_object in module_items:
                module_item = vars(module_item_object)
                updated_module_item = update_parameters(module_item, MODULE_ITEM_REQUIRED_PARAMETERS, MODULE_ITEM_OPTIONAL_PARAMETERS)

                # Remove module item from list and append updated version
                updated_module_items.append(updated_module_item)
            
            updated_module.update({'items': updated_module_items})
            updated_modules.append(updated_module)
        return updated_modules

    # Parse Assignment Groups
    def parse_assignment_groups(self):
        """
        :rtype: List[dict]
        """
        assignment_groups = self.course.get_assignment_groups()
        updated_assignment_groups = []
        for assignment_group in assignment_groups:
            assignment_group_dict = vars(assignment_group)
            updated_assignment_group = update_parameters(assignment_group_dict, ASSIGNMENT_GROUP_REQUIRED_PARAMETERS, ASSIGNMENT_GROUP_OPTIONAL_PARAMETERS)
            updated_assignment_groups.append(updated_assignment_group)
        return updated_assignment_groups

    # Parse Assignments
    def parse_assignments(self):
        """
        :rtype: List[dict]
        """
        assigments = self.course.get_assignments()
        updated_assignments = []
        for assignment in assigments:
            assignment_dict = vars(assignment)
            updated_assignment = update_parameters(assignment_dict, ASSIGNMENT_REQUIRED_PARAMETERS, ASSIGNMENT_OPTIONAL_PARAMETERS)
            updated_assignments.append(updated_assignment)
        return updated_assignments

    # Parse Discussion Topics
    def parse_discussion_topics(self):
        """
        :rtype: List[dict]
        """
        discussion_topics = self.course.get_discussion_topics()
        updated_discussion_topics = []
        for discussion_topic in discussion_topics:
            discussion_topic_dict = vars(discussion_topic)
            updated_discussion_topic = update_parameters(discussion_topic_dict, DISCUSSION_TOPIC_REQUIRED_PARAMETERS, DISCUSSION_TOPIC_OPTIONAL_PARAMETERS)
            updated_discussion_topics.append(updated_discussion_topic)
        return updated_discussion_topics

    # Parse Pages
    def parse_pages(self):
        """
        :rtype: List[dict]
        """
        pages = self.course.get_pages()
        updated_pages = []
        for page in pages:
            page_dict = vars(page)
            updated_page = update_parameters(page_dict, PAGE_REQUIRED_PARAMETERS, PAGE_OPTIONAL_PARAMETERS)
            updated_pages.append(updated_page)
        return updated_pages

    # Write to filename
    def course_to_json(self, filename):
        """
        :type filename: str
        :rtype: None
        """
        course_dict = {
            'modules': self.parse_modules(),
            'assignment_groups': self.parse_assignment_groups(),
            'assignments': self.parse_assignments(),
            'discussion_topics': self.parse_discussion_topics(),
            'pages': self.parse_pages()
            }
        course_json = json.dumps(course_dict, indent = 4, default = str)
        with open(filename, 'w') as outfile:
            outfile.write(course_json)
            print("wrote to", filename)