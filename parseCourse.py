from canvasapi import Canvas
from canvasParameters import *
import json
import os


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
    def __init__(self, id, course):
        """
        This class maintains a map of temporary ids.

        Attributes:
            id (int): The course id used to create the course
            course (canvasapi.course.Course): The course that is being parsed
            temporary_ids (dict): Map of content ids to temporary ids
        """
        
        self.id = id
        self.course = course
        self.temp_ids = {}
        self.temp_ids_counter = 0

    # Generate new temp id
    def get_new_id(self):
        """
        This method returns a new 5 digit temporary id and increments total ids by one.

        Keyword arguments:
        Return: string
        """
        self.temp_ids_counter += 1
        return str(self.temp_ids_counter).zfill(5)

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
            for module_item in module_items:
                module_item_dict = vars(module_item)
                updated_module_item = update_parameters(module_item_dict, MODULE_ITEM_REQUIRED_PARAMETERS, MODULE_ITEM_OPTIONAL_PARAMETERS)
                
                # Link module item ids if exist
                if 'content_id' in module_item_dict and not module_item_dict['content_id'] is None and module_item_dict['content_id'] in self.temp_ids:
                    updated_module_item.update({'item_temp_id': self.temp_ids[module_item_dict['content_id']]})

                # Remove module item from list and append updated version
                updated_module_items.append(updated_module_item)
            
            # Generate new 5 digit temp id based on module position
            temp_id = str(updated_module['position']).zfill(5)
            updated_module.update({'temp_id': temp_id})

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

            # Create temporary id for assignment group
            if not assignment_group_dict['id'] in self.temp_ids:
                self.temp_ids.update({assignment_group_dict['id']: self.get_new_id()})
            
            updated_assignment_group.update({'temp_id': self.temp_ids[assignment_group_dict['id']]})

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
            
            # Create temporary id for assignment
            if not assignment_dict['id'] in self.temp_ids:
                self.temp_ids.update({assignment_dict['id']: self.get_new_id()})
            
            updated_assignment.update({'temp_id': self.temp_ids[assignment_dict['id']]})

            # Link assignment group ids if exist
            if not assignment_dict['assignment_group_id'] is None and assignment_dict['assignment_group_id'] in self.temp_ids:
                updated_assignment.update({'assignment_group_temp_id': self.temp_ids[assignment_dict['assignment_group_id']]})
            
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

            # Create temporary id for discussion
            if not discussion_topic_dict['id'] in self.temp_ids:
                self.temp_ids.update({discussion_topic_dict['id']: self.get_new_id()})
            
            updated_discussion_topic.update({'temp_id': self.temp_ids[discussion_topic_dict['id']]})

            # Link assignment temp id if exists
            if not discussion_topic_dict['assignment_id'] is None and discussion_topic_dict['assignment_id'] in self.temp_ids:
                updated_discussion_topic.update({'assignment_temp_id': self.temp_ids[discussion_topic_dict['assignment_id']]})

            updated_discussion_topics.append(updated_discussion_topic)

        return updated_discussion_topics

    # Writes dict to json
    def write_to_json(self, filename, dict_to_write):
        """
        Writes to json file with given filename and dictionary
        
        Keyword arguments:
        filename -- string
        dict_to_write -- string
        Return: None
        """
        dict_json = json.dumps(dict_to_write, indent=4, default=str)
        with open(filename, 'w') as outfile:
            outfile.write(dict_json)

    # Write to new folder under SavedCourses/CNVS{$id}
    def course_to_json(self):
        """
        :rtype: None
        """
        # Create folder to store course files in
        parent_dir = os.path.join('./SavedCourses', 'CNVS_C' + str(self.id))

        # Clear everything in foler if there is already a folder
        if os.path.exists(parent_dir):
            for filename in os.listdir(parent_dir):
                os.remove(os.path.join(parent_dir, filename))
        else:
            os.mkdir(parent_dir)

        # Create assignment group files, needs to go before assignments to put all ids
        for assignment_group in self.parse_assignment_groups():
            filename = "CNVS_G" + assignment_group['temp_id'] + '.json'
            self.write_to_json(os.path.join(parent_dir, filename), assignment_group)
        
        # Create assignment files, needs to go before discussions to put all ids
        for assignment in self.parse_assignments():
            filename = "CNVS_A" + assignment['temp_id'] + '.json'
            self.write_to_json(os.path.join(parent_dir, filename), assignment)

        # Create discussion files
        for discussion_topic in self.parse_discussion_topics():
            filename = "CNVS_D" + discussion_topic['temp_id'] + '.json'
            self.write_to_json(os.path.join(parent_dir, filename), discussion_topic)
        
        # Create module files
        for module in self.parse_modules():
            filename = "CNVS_M" + module['temp_id'] + '.json'
            self.write_to_json(os.path.join(parent_dir, filename), module)
        
        print("Course parsing has concluded.")