from canvasapi import Canvas
from parseCourse import CourseParser
import configparser
import os

class CanvasUser:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
            self.canvas = Canvas(self.parser['CANVAS CLONE']['api_url'], self.parser['CANVAS CLONE']['api_key'])
        else:
            API_URL = input('API URL: ')
            API_KEY = input('API Token: ')
            self.parser['CANVAS CLONE'] = {}
            self.parser['CANVAS CLONE']['api_url'] = API_URL
            self.parser['CANVAS CLONE']['api_key'] = API_KEY
            with open("config.ini", "w") as configfile:
                self.parser.write(configfile)
            self.canvas = Canvas(API_URL, API_KEY)
        user = self.canvas.get_current_user()
        print(f"Connected to Canvas as {user.name} ({user.id})")
    

def main():
    canvas = CanvasUser().canvas
    id = 1558121
    course = canvas.get_course(id)
    parser = CourseParser(id, course)
    parser.course_to_json()

if __name__ == '__main__':
    main()