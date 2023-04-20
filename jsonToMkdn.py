from markdownify import markdownify as md
import configparser
import json
import re
import os
import requests


        

class MkdnParser:

    def check_links(self, s):
        """
        Checks if the given link is a canvas file, if so, downloads the file and gives a path to the file
        
        Keyword arguments:
        s -- re.Match object containing a link
        Return: string
        """
        link = s.group(1)
        print(link)
        filename = s.group(2)
        print(filename)
        r = requests.get(link, auth = (self.parser['CANVAS CLONE']['api_key'],))

    def __init__(self, file):
        # Get api key for making file download requests later
        self.parser = configparser.ConfigParser()
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            API_URL = input('API URL: ')
            API_KEY = input('API Token: ')
            self.parser['CANVAS CLONE'] = {}
            self.parser['CANVAS CLONE']['api_url'] = API_URL
            self.parser['CANVAS CLONE']['api_key'] = API_KEY
            with open("config.ini", "w") as configfile:
                self.parser.write(configfile)

        self.file = file
        with open(file) as infile:
            self.file_dict = json.load(infile)

    def clean_description(self):
        """
        Removes newline characters from the description in the assignment json
        
        Keyword arguments:
        Return: None
        """
        self.file_dict.update({'description': self.file_dict['description'].replace(r'\n', '')})

    def parse_links_to_files(self):
        """
        Takes json structure of assignment and takes files, downloads them and changes the locations in the json
        
        Keyword arguments:
        Return: None
        """
        linkPattern = r'<a[^>]*?href="([^"]*)"[^>]*>([^<]*)'

        linkTags = re.sub(linkPattern, self.check_links, self.file_dict['description'])
        # print(linkTags)

    def write_to_mkdn(self, filename):
        """
        Opens the file, reads the file and writes it to markdown
        
        Keyword arguments:
        filename -- string, file to write to
        Return: None
        """
        file_mkdn = ''
        file_mkdn += 'CRT_HW START ' + self.file_dict['name'] + '\n'

        file_mkdn += md(self.file_dict['description'], autolinks = False, escape_asterisks = False, escape_underscores = False, heading_style = 'ATX', strip = ['ul'])

        file_mkdn += '\nCRT_HW END'
        file_mkdn_encoded = bytes(file_mkdn, 'utf-8')

        with open(filename, 'wb') as outfile:
            outfile.write(file_mkdn_encoded)
        
def main():
    parser = MkdnParser('./CodEvalTooling/CNVS_A00024.json')
    if not os.path.exists('./CodEvalTooling/'):
        os.makedirs('./CodEvalTooling/')
    
    parser.clean_description()
    parser.parse_links_to_files()

    parser.write_to_mkdn('./CodEvalTooling/PA 01.txt')

if __name__ == '__main__':
    main()